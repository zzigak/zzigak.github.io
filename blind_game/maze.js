const startButton = document.getElementById("startButton");
const retryMapButton = document.getElementById("retryMapButton");
const newMazeButton = document.getElementById("newMazeButton");
const replayButton = document.getElementById("replayButton");
const toggleMapButton = document.getElementById("toggleMapButton");
const mazeSizeSelect = document.getElementById("mazeSizeSelect");
const voiceSelect = document.getElementById("voiceSelect");
const intervalSlider = document.getElementById("intervalSlider");
const intervalValue = document.getElementById("intervalValue");
const facingSlider = document.getElementById("facingSlider");
const facingLabel = document.getElementById("facingLabel");
const guideDirectionLabel = document.getElementById("guideDirectionLabel");
const distanceLabel = document.getElementById("distanceLabel");
const mazeStatusLabel = document.getElementById("mazeStatusLabel");
const currentTimeLabel = document.getElementById("currentTimeLabel");
const sameMapTotalLabel = document.getElementById("sameMapTotalLabel");
const mapIdLabel = document.getElementById("mapIdLabel");
const wallHitRateLabel = document.getElementById("wallHitRateLabel");
const runReplaySelect = document.getElementById("runReplaySelect");
const vizSection = document.getElementById("vizSection");
const canvas = document.getElementById("topDownCanvas");
const ctx = canvas.getContext("2d");
const onboardingScreen = document.getElementById("onboardingScreen");
const onboardingLanguage = document.getElementById("onboardingLanguage");
const onboardingTitle = document.getElementById("onboardingTitle");
const onboardingContext = document.getElementById("onboardingContext");
const onboardingSafety = document.getElementById("onboardingSafety");
const onboardingHowTo = document.getElementById("onboardingHowTo");
const enterGameButton = document.getElementById("enterGameButton");
const gamePanel = document.getElementById("gamePanel");

const DEFAULT_MAZE_SIZE = 13;
const MOVE_STEP = 1;
const PLAYER_RADIUS = 0.16;
const WALL_THICKNESS = 0.13;
const CARDINAL_LABELS = ["North", "East", "South", "West"];
/** Only two voices: Chinese (ara) vs Japanese-style one-shots + Anna long loop. */
const VOICE_PACKS = {
  chinese: {
    guide: [
      ["./audio/ara_ara_big_sister_01_this_way.wav"],
      ["./audio/ara_ara_big_sister_01_over_here.wav"],
      ["./audio/ara_ara_big_sister_01_come_here.wav"],
      ["./audio/ara_ara_big_sister_04_quickly_lets_go.wav"],
    ],
    intro: ["./audio/ara_ara_big_sister_00_intro.wav"],
    continuous: "./audio/ara_ara_big_sister_001.wav",
  },
  japanese: {
    guide: [
      ["./audio/calm_shrine_style_01_this_way.wav"],
      ["./audio/calm_shrine_style_01_over_here.wav"],
      ["./audio/calm_shrine_style_01_come_here.wav"],
      ["./audio/calm_shrine_style_04_quickly_lets_go.wav"],
    ],
    intro: ["./audio/calm_shrine_style_00_intro.wav"],
    continuous: "./audio/Ono_Anna_001.wav",
  },
};

let audioCtx = null;
let toneFilter = null;
let distanceToneGain = null;
let panner = null;
let guideClipBuffers = [];
let guideClipIndex = 0;
let introClipBuffer = null;
let continuousGuideElement = null;
let continuousGuideMediaNode = null;
let continuousGuideGain = null;

/** Must run synchronously during a user gesture — see startButton handler. */
function resumeAudioContextSync() {
  if (!audioCtx || audioCtx.state === "running") return;
  
  void audioCtx.resume();
}
let pulseTimerId = null;
let activePulseIntervalMs = null;
let pulsePeak = 0.45;
let pulseIntervalMs = 2400;

let facingDegrees = 0;
let mazeSize = DEFAULT_MAZE_SIZE;
let maze = [];
let mazeSnapshot = [];
let player = { x: 1.5, y: 1.5 };
let goal = { x: mazeSize - 1.5, y: mazeSize - 1.5 };
let guide = { x: 1.5, y: 1.5 };
let mazeCompleted = false;
let mapVisible = false;
let runActive = false;
let demoRoundActive = false;
let demoTransitionPending = false;
let demoRoundCompleted = false;

let currentMapId = 1;
let sameMapTotalMs = 0;
let currentRunStartedAtMs = 0;
let completedRunMs = 0;
let runTickerId = null;
let currentRunTrace = [];
let lastCompletedTrace = [];
let lastCompletedTraceDurationMs = 0;
let currentRunPulseEvents = [];
let lastCompletedPulseEvents = [];
let replayTimerId = null;
let replayActive = false;
let replayCursorMs = 0;
let runHistory = [];
let runHistoryCounter = 1;
let currentRunStepAttempts = 0;
let currentRunWallHits = 0;
let safetyPromptShown = false;

const ONBOARDING_COPY = {
  zh: {
    title: "音频迷宫",
    context:
      "这是一个依靠空间音频导航的迷宫。第一局是演示局（地图可见），通关后进入正式局（默认隐藏地图）。",
    safety:
      "开始认真游玩前，请闭眼或戴上眼罩，只用声音来判断方向。",
    howTo:
      "进入游戏后点击 Start Audio。使用 W/A/S/D 移动，左右方向键旋转。语音可在 Controls 里切换（中文 / 日语）。重玩、地图和回放在 Controls 里。",
    enter: "进入游戏面板",
  },
  ja: {
    title: "オーディオ迷路",
    context:
      "この迷路は立体音響で進みます。1回目は地図ありのデモ、クリア後は地図非表示の本番モードになります。",
    safety:
      "本番プレイでは、目を閉じるかアイマスクを着けて、音だけで進んでください。",
    howTo:
      "ゲーム画面で Start Audio を押します。W/A/S/D で移動、左右キーで回転。音声は Controls で中文/日本語を切り替えできます。設定とリプレイは Controls にあります。",
    enter: "ゲーム画面へ進む",
  },
};

function clampAngle(value) {
  const normalized = value % 360;
  return normalized < 0 ? normalized + 360 : normalized;
}

function distance2d(ax, ay, bx, by) {
  const dx = ax - bx;
  const dy = ay - by;
  return Math.sqrt(dx * dx + dy * dy);
}

function formatTime(ms) {
  const totalTenths = Math.floor(ms / 100);
  const tenths = totalTenths % 10;
  const totalSeconds = Math.floor(totalTenths / 10);
  const seconds = totalSeconds % 60;
  const minutes = Math.floor(totalSeconds / 60);
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}.${tenths}`;
}

function updateTimerHud() {
  const currentMs = runActive
    ? mazeCompleted
      ? completedRunMs
      : Math.max(0, Date.now() - currentRunStartedAtMs)
    : 0;
  currentTimeLabel.textContent = formatTime(currentMs);
  sameMapTotalLabel.textContent = formatTime(sameMapTotalMs);
  mapIdLabel.textContent = `#${currentMapId}`;
  const hitRate = currentRunStepAttempts > 0 ? (currentRunWallHits / currentRunStepAttempts) * 100 : 0;
  wallHitRateLabel.textContent = `${hitRate.toFixed(1)}% (${currentRunWallHits}/${currentRunStepAttempts})`;
}

function renderOnboarding(languageKey) {
  const lang = ONBOARDING_COPY[languageKey] ? languageKey : "zh";
  const copy = ONBOARDING_COPY[lang];
  onboardingTitle.textContent = copy.title;
  onboardingContext.textContent = copy.context;
  onboardingSafety.textContent = copy.safety;
  onboardingHowTo.textContent = copy.howTo;
  enterGameButton.textContent = copy.enter;
}

function getContinuousGuideTrack() {
  const key = getSelectedVoicePackKey();
  const pack = VOICE_PACKS[key];
  return pack?.continuous || VOICE_PACKS.chinese.continuous;
}

function startRunTimer() {
  if (runTickerId) clearInterval(runTickerId);
  currentRunStartedAtMs = Date.now();
  completedRunMs = 0;
  currentRunStepAttempts = 0;
  currentRunWallHits = 0;
  currentRunTrace = [{ t: 0, x: player.x, y: player.y, dir: facingDegrees }];
  currentRunPulseEvents = [];
  runTickerId = setInterval(() => {
    updateTimerHud();
    recordRunPoint();
  }, 100);
  updateTimerHud();
}

function stopRunTimer() {
  if (runTickerId) {
    clearInterval(runTickerId);
    runTickerId = null;
  }
  completedRunMs = Math.max(0, Date.now() - currentRunStartedAtMs);
  recordRunPoint(true);
  if (currentRunTrace.length > 1) {
    lastCompletedTrace = currentRunTrace.map((point) => ({ ...point }));
    lastCompletedTraceDurationMs = completedRunMs;
    lastCompletedPulseEvents = currentRunPulseEvents.map((event) => ({ ...event }));
    replayButton.disabled = false;
    const run = {
      id: runHistoryCounter++,
      mapId: currentMapId,
      durationMs: completedRunMs,
      stepAttempts: currentRunStepAttempts,
      wallHits: currentRunWallHits,
      trace: lastCompletedTrace.map((point) => ({ ...point })),
      pulseEvents: lastCompletedPulseEvents.map((event) => ({ ...event })),
    };
    runHistory.push(run);
    updateReplaySelectOptions(run.id);
  }
  updateTimerHud();
}

function resetCurrentTimerDisplay() {
  completedRunMs = 0;
  currentRunStartedAtMs = Date.now();
  currentRunStepAttempts = 0;
  currentRunWallHits = 0;
  updateTimerHud();
}

function recordRunPoint(force = false) {
  if (!runActive) return;
  const t = Math.max(0, Date.now() - currentRunStartedAtMs);
  const last = currentRunTrace[currentRunTrace.length - 1];
  if (!last) {
    currentRunTrace.push({ t, x: player.x, y: player.y, dir: facingDegrees });
    return;
  }
  const dist = distance2d(last.x, last.y, player.x, player.y);
  const dirChanged = last.dir !== facingDegrees;
  if (force || dist > 0.03 || t - last.t > 220 || dirChanged) {
    currentRunTrace.push({ t, x: player.x, y: player.y, dir: facingDegrees });
  }
}

function stopReplay() {
  if (replayTimerId) {
    clearInterval(replayTimerId);
    replayTimerId = null;
  }
  replayActive = false;
  replayCursorMs = 0;
}

function updateReplaySelectOptions(selectedRunId = null) {
  runReplaySelect.innerHTML = "";
  if (runHistory.length === 0) {
    const option = document.createElement("option");
    option.textContent = "No runs yet";
    option.value = "";
    runReplaySelect.appendChild(option);
    runReplaySelect.disabled = true;
    replayButton.disabled = true;
    return;
  }
  runReplaySelect.disabled = false;
  for (const run of runHistory) {
    const option = document.createElement("option");
    option.value = String(run.id);
    option.textContent = `Run ${run.id} | Map ${run.mapId} | ${formatTime(run.durationMs)}`;
    runReplaySelect.appendChild(option);
  }
  const fallback = runHistory[runHistory.length - 1].id;
  runReplaySelect.value = String(selectedRunId ?? fallback);
  replayButton.disabled = false;
}

function getSelectedRunForReplay() {
  if (runHistory.length === 0) return null;
  const selectedId = Number(runReplaySelect.value);
  return runHistory.find((run) => run.id === selectedId) || runHistory[runHistory.length - 1];
}

function createMaze(width, height) {
  const grid = Array.from({ length: height }, () => Array(width).fill(1));
  function shuffle(values) {
    const copy = [...values];
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }
  function carve(x, y) {
    grid[y][x] = 0;
    const dirs = shuffle([
      [2, 0],
      [-2, 0],
      [0, 2],
      [0, -2],
    ]);
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx <= 0 || ny <= 0 || nx >= width - 1 || ny >= height - 1) continue;
      if (grid[ny][nx] !== 1) continue;
      grid[y + dy / 2][x + dx / 2] = 0;
      carve(nx, ny);
    }
  }
  carve(1, 1);
  grid[1][1] = 0;
  grid[height - 2][width - 2] = 0;
  return grid;
}

function cloneMaze(src) {
  return src.map((row) => [...row]);
}

function isWallAt(x, y) {
  const gridX = Math.floor(x);
  const gridY = Math.floor(y);
  if (gridX < 0 || gridY < 0 || gridX >= mazeSize || gridY >= mazeSize) return true;
  return maze[gridY][gridX] === 1;
}

function canMoveTo(x, y) {
  return (
    !isWallAt(x - PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x - PLAYER_RADIUS, y + PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y + PLAYER_RADIUS)
  );
}

function getPlayerCell() {
  return { x: Math.floor(player.x), y: Math.floor(player.y) };
}

function getGoalCell() {
  return { x: Math.floor(goal.x), y: Math.floor(goal.y) };
}

function getCellKey(x, y) {
  return `${x},${y}`;
}

function computePathBfs(startCell, endCell) {
  const queue = [startCell];
  const visited = new Set([getCellKey(startCell.x, startCell.y)]);
  const parent = new Map();
  const moves = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
  ];
  while (queue.length) {
    const current = queue.shift();
    if (current.x === endCell.x && current.y === endCell.y) break;
    for (const [dx, dy] of moves) {
      const nx = current.x + dx;
      const ny = current.y + dy;
      if (nx < 0 || ny < 0 || nx >= mazeSize || ny >= mazeSize) continue;
      if (maze[ny][nx] === 1) continue;
      const key = getCellKey(nx, ny);
      if (visited.has(key)) continue;
      visited.add(key);
      parent.set(key, current);
      queue.push({ x: nx, y: ny });
    }
  }
  const endKey = getCellKey(endCell.x, endCell.y);
  if (!visited.has(endKey)) return [];
  const path = [];
  let current = endCell;
  while (current) {
    path.push(current);
    current = parent.get(getCellKey(current.x, current.y)) || null;
  }
  path.reverse();
  return path;
}

function chooseGuideCellFromPath(path) {
  if (path.length <= 1) return path[0] || getGoalCell();
  if (path.length === 2) return path[1];
  const initialDx = path[1].x - path[0].x;
  const initialDy = path[1].y - path[0].y;
  let index = 1;
  while (index + 1 < path.length) {
    const nextDx = path[index + 1].x - path[index].x;
    const nextDy = path[index + 1].y - path[index].y;
    if (nextDx !== initialDx || nextDy !== initialDy) return path[index];
    index += 1;
  }
  return path[path.length - 1];
}

function updateGuideWaypoint() {
  const path = computePathBfs(getPlayerCell(), getGoalCell());
  const waypointCell = chooseGuideCellFromPath(path);
  guide = { x: waypointCell.x + 0.5, y: waypointCell.y + 0.5 };
}

function getDistanceToGoal() {
  return distance2d(player.x, player.y, goal.x, goal.y);
}

function getDistanceToGuide() {
  return distance2d(player.x, player.y, guide.x, guide.y);
}

function getRelativeDirectionLabel() {
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const rightX = Math.cos(facingRad);
  const rightY = Math.sin(facingRad);
  const forwardComponent = toGuideX * forwardX + toGuideY * forwardY;
  const rightComponent = toGuideX * rightX + toGuideY * rightY;
  const relative = Math.atan2(rightComponent, forwardComponent);
  const sector = Math.round(relative / (Math.PI / 4));
  const labels = [
    "Forward",
    "Forward-Right",
    "Right",
    "Back-Right",
    "Back",
    "Back-Left",
    "Left",
    "Forward-Left",
  ];
  return labels[((sector % 8) + 8) % 8];
}

function getFacingVectors() {
  const idx = ((Math.round(facingDegrees / 90) % 4) + 4) % 4;
  const forward = [
    { x: 0, y: -1 },
    { x: 1, y: 0 },
    { x: 0, y: 1 },
    { x: -1, y: 0 },
  ][idx];
  const right = [
    { x: 1, y: 0 },
    { x: 0, y: 1 },
    { x: -1, y: 0 },
    { x: 0, y: -1 },
  ][idx];
  return { forward, right };
}

function updateFacingLabel() {
  const cardinalIndex = Math.round(facingDegrees / 90) % 4;
  facingLabel.textContent = `${Math.round(facingDegrees)}° (${CARDINAL_LABELS[cardinalIndex]})`;
}

function updateGuideAudio() {
  if (!audioCtx || !panner || !distanceToneGain || !toneFilter || mazeCompleted) return;
  const now = audioCtx.currentTime;
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const distance = getDistanceToGuide();
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const frontness = Math.max(
    -1,
    Math.min(1, (toGuideX * forwardX + toGuideY * forwardY) / Math.max(distance, 0.001))
  );

  panner.positionX.setValueAtTime(toGuideX, now);
  panner.positionY.setValueAtTime(0, now);
  panner.positionZ.setValueAtTime(toGuideY, now);

  // Use 1 cell as loudness reference: no distance attenuation at or inside that range.
  const overReference = Math.max(0, distance - 1);
  const distanceFactor = Math.max(0.88, 1 - overReference * 0.02);
  const nearBoost = distance < 0.7 ? Math.min(0.06, (0.7 - distance) * 0.12) : 0;
  const frontScale = (frontness + 1) / 2;
  const directionalGain = 0.62 + frontScale * 0.38;
  const guideGainTarget = (distanceFactor + nearBoost) * directionalGain;
  distanceToneGain.gain.setTargetAtTime(guideGainTarget, now, 0.04);
  // Keep the repeating guide call bright/clear, closer to the intro callout timbre.
  toneFilter.frequency.setTargetAtTime(4200, now, 0.06);
  pulsePeak = 0.45;
  if (continuousGuideGain) {
    if (!runActive || mazeCompleted) {
      continuousGuideGain.gain.setTargetAtTime(0.0001, now, 0.04);
    } else {
      const volumeTarget = Math.max(0.08, Math.min(1, pulsePeak));
      continuousGuideGain.gain.setTargetAtTime(volumeTarget, now, 0.04);
    }
  }
}

function updateListener() {
  if (!audioCtx) return;
  const listener = audioCtx.listener;
  const rad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(rad);
  const forwardZ = -Math.cos(rad);
  if (listener.positionX) {
    listener.positionX.setValueAtTime(0, audioCtx.currentTime);
    listener.positionY.setValueAtTime(0, audioCtx.currentTime);
    listener.positionZ.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardX.setValueAtTime(forwardX, audioCtx.currentTime);
    listener.forwardY.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardZ.setValueAtTime(forwardZ, audioCtx.currentTime);
    listener.upX.setValueAtTime(0, audioCtx.currentTime);
    listener.upY.setValueAtTime(1, audioCtx.currentTime);
    listener.upZ.setValueAtTime(0, audioCtx.currentTime);
  } else if (listener.setOrientation) {
    listener.setPosition(0, 0, 0);
    listener.setOrientation(forwardX, 0, forwardZ, 0, 1, 0);
  }
}

function stopContinuousGuideVoice() {
  if (continuousGuideGain && audioCtx) {
    continuousGuideGain.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.03);
  } else if (continuousGuideElement) {
    continuousGuideElement.volume = 0;
  }
}

function ensureContinuousGuideVoice() {
  if (!audioCtx || !runActive || mazeCompleted) {
    return;
  }
  resumeAudioContextSync();
  if (!continuousGuideElement) {
    continuousGuideElement = new Audio(getContinuousGuideTrack());
    continuousGuideElement.loop = true;
    continuousGuideElement.preload = "auto";
    continuousGuideElement.volume = 1;
  }
  if (!continuousGuideMediaNode && audioCtx) {
    continuousGuideMediaNode = audioCtx.createMediaElementSource(continuousGuideElement);
    continuousGuideGain = audioCtx.createGain();
    continuousGuideGain.gain.value = 0.0001;
    continuousGuideMediaNode.connect(continuousGuideGain);
    continuousGuideGain.connect(toneFilter);
  }
  const playPromise = continuousGuideElement.play();
  if (playPromise?.catch) {
    playPromise.catch(() => {
      // Ignore autoplay races; next user-gesture tick will resume.
    });
  }
}

function pulseGuide() {
  ensureContinuousGuideVoice();
}

function updatePulseLoop() {
  if (runActive && !mazeCompleted) {
    ensureContinuousGuideVoice();
  }
}

function updateGuideState() {
  updateGuideWaypoint();
  guideDirectionLabel.textContent = getRelativeDirectionLabel();
  distanceLabel.textContent = `${getDistanceToGuide().toFixed(1)} cells`;
  if (mazeCompleted) {
    mazeStatusLabel.textContent = "Goal reached";
  } else if (!runActive) {
    mazeStatusLabel.textContent = "Tutorial in progress";
  } else {
    mazeStatusLabel.textContent = "Follow the guide";
  }
  updateGuideAudio();
  updatePulseLoop();
}

function checkGoal() {
  if (mazeCompleted || !runActive) return;
  if (getDistanceToGoal() <= 0.5) {
    mazeCompleted = true;
    mazeStatusLabel.textContent = "Goal reached";
    guideDirectionLabel.textContent = "Done";
    stopRunTimer();
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
    }
    stopContinuousGuideVoice();
    if (demoRoundActive) {
      beginRealGameAfterDemo();
    }
  }
}

function playBumpSound() {
  if (!audioCtx) return;
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = "triangle";
  osc.frequency.setValueAtTime(120, now);
  osc.frequency.exponentialRampToValueAtTime(85, now + 0.08);
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(0.09, now + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.1);
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(now);
  osc.stop(now + 0.11);
}

function playStepSound() {
  if (!audioCtx) return;
  const now = audioCtx.currentTime;
  const noiseBuffer = audioCtx.createBuffer(1, Math.floor(audioCtx.sampleRate * 0.05), audioCtx.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < data.length; i += 1) {
    data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
  }

  const source = audioCtx.createBufferSource();
  source.buffer = noiseBuffer;

  const filter = audioCtx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.setValueAtTime(650, now);
  filter.Q.value = 0.7;

  const gain = audioCtx.createGain();
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(0.05, now + 0.006);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.07);

  source.connect(filter);
  filter.connect(gain);
  gain.connect(audioCtx.destination);
  source.start(now);
  source.stop(now + 0.075);
}

function movePlayer(localX, localY) {
  if (mazeCompleted || !runActive || replayActive) return;
  currentRunStepAttempts += 1;
  const cellX = Math.floor(player.x);
  const cellY = Math.floor(player.y);
  const { forward, right } = getFacingVectors();
  const stepForward = -localY;
  const dx = right.x * localX + forward.x * stepForward;
  const dy = right.y * localX + forward.y * stepForward;
  const nextCellX = cellX + dx;
  const nextCellY = cellY + dy;

  if (
    nextCellX < 0 ||
    nextCellY < 0 ||
    nextCellX >= mazeSize ||
    nextCellY >= mazeSize ||
    maze[nextCellY][nextCellX] === 1
  ) {
    currentRunWallHits += 1;
    playBumpSound();
    updateTimerHud();
    return;
  }

  player.x = nextCellX + 0.5;
  player.y = nextCellY + 0.5;
  playStepSound();
  checkGoal();
  recordRunPoint();
  updateGuideState();
  drawMaze();
  updateTimerHud();
}

function getSelectedVoicePackKey() {
  const selected = voiceSelect?.value || "chinese";
  return VOICE_PACKS[selected] ? selected : "chinese";
}

async function decodeFirstAvailable(candidates) {
  if (!audioCtx) return null;
  for (const url of candidates) {
    try {
      const response = await fetch(url);
      if (!response.ok) continue;
      return await audioCtx.decodeAudioData(await response.arrayBuffer());
    } catch {
      // Try next URL candidate for this clip slot.
    }
  }
  return null;
}

async function loadPackBuffers(pack) {
  const guide = [];
  for (const slot of pack.guide) {
    const decoded = await decodeFirstAvailable(slot);
    if (decoded) guide.push(decoded);
  }
  const intro = await decodeFirstAvailable(pack.intro);
  return { guide, intro };
}

async function loadGuideClipBuffer(forceReload = false) {
  if (!audioCtx) return;
  if (!forceReload && guideClipBuffers.length > 0) return;

  guideClipBuffers = [];
  guideClipIndex = 0;
  introClipBuffer = null;

  const selectedKey = getSelectedVoicePackKey();
  const loaded = await loadPackBuffers(VOICE_PACKS[selectedKey]);
  guideClipBuffers = loaded.guide;
  introClipBuffer = loaded.intro;

  if (guideClipBuffers.length === 0) {
    mazeStatusLabel.textContent = `No guide clips found for voice: ${selectedKey}`;
  }
}

async function initializeAudio() {
  // AudioContext and continuous voice chain are set up synchronously in the
  // click handler before this is called, so this is a no-op on first run.
  if (!audioCtx) return;
  await loadGuideClipBuffer();
  if (guideClipBuffers.length === 0) mazeStatusLabel.textContent = "Could not load guide clip";
}

function drawMaze() {
  const width = canvas.width;
  const height = canvas.height;
  const cellW = width / mazeSize;
  const cellH = height / mazeSize;
  const wallInset = Math.min(cellW, cellH) * WALL_THICKNESS;
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, width, height);
  for (let y = 0; y < mazeSize; y += 1) {
    for (let x = 0; x < mazeSize; x += 1) {
      if (maze[y]?.[x] !== 1) continue;
      ctx.fillStyle = "#1f1f1f";
      ctx.fillRect(
        x * cellW + wallInset,
        y * cellH + wallInset,
        cellW - wallInset * 2,
        cellH - wallInset * 2
      );
    }
  }
  const goalX = goal.x * cellW;
  const goalY = goal.y * cellH;
  const guideX = guide.x * cellW;
  const guideY = guide.y * cellH;
  ctx.fillStyle = mazeCompleted ? "#8ae68a" : "#10b981";
  ctx.beginPath();
  ctx.arc(goalX, goalY, Math.min(cellW, cellH) * 0.22, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#f97316";
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.28, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "#f97316";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.48, 0, Math.PI * 2);
  ctx.stroke();
  const px = player.x * cellW;
  const py = player.y * cellH;
  ctx.fillStyle = "#fff";
  ctx.beginPath();
  ctx.arc(px, py, Math.min(cellW, cellH) * 0.24, 0, Math.PI * 2);
  ctx.fill();
  const rad = (facingDegrees * Math.PI) / 180;
  const arrowLength = Math.min(cellW, cellH) * 0.7;
  ctx.strokeStyle = "#e5e5e5";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(px, py);
  ctx.lineTo(px + Math.sin(rad) * arrowLength, py - Math.cos(rad) * arrowLength);
  ctx.stroke();

  if (replayActive && lastCompletedTrace.length > 1) {
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2;
    ctx.beginPath();
    let started = false;
    for (const point of lastCompletedTrace) {
      if (point.t > replayCursorMs) break;
      const tx = point.x * cellW;
      const ty = point.y * cellH;
      if (!started) {
        ctx.moveTo(tx, ty);
        started = true;
      } else {
        ctx.lineTo(tx, ty);
      }
    }
    if (started) ctx.stroke();

    const ghost = sampleReplayAt(replayCursorMs);
    if (ghost) {
      const gx = ghost.x * cellW;
      const gy = ghost.y * cellH;
      const ghostDir = Number.isFinite(ghost.dir) ? ghost.dir : 0;
      ctx.fillStyle = "#67e8f9";
      ctx.beginPath();
      ctx.arc(gx, gy, Math.min(cellW, cellH) * 0.2, 0, Math.PI * 2);
      ctx.fill();

      const r = Math.min(cellW, cellH) * 0.55;
      const dirRad = (ghostDir * Math.PI) / 180;
      ctx.strokeStyle = "#a5f3fc";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(gx, gy);
      ctx.lineTo(gx + Math.sin(dirRad) * r, gy - Math.cos(dirRad) * r);
      ctx.stroke();
    }

    const pulseEvent = getReplayPulseEventAt(replayCursorMs);
    if (pulseEvent) {
      const fx = pulseEvent.x * cellW;
      const fy = pulseEvent.y * cellH;
      const blinkT = 1 - (replayCursorMs - pulseEvent.t) / 190;
      ctx.strokeStyle = `rgba(251, 146, 60, ${Math.max(0.25, blinkT)})`;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(
        fx,
        fy,
        Math.min(cellW, cellH) * (0.55 + (1 - blinkT) * 0.35),
        0,
        Math.PI * 2
      );
      ctx.stroke();
    }
  }
}

function sampleReplayAt(timeMs) {
  if (lastCompletedTrace.length === 0) return null;
  if (timeMs <= 0) return lastCompletedTrace[0];
  if (timeMs >= lastCompletedTraceDurationMs) return lastCompletedTrace[lastCompletedTrace.length - 1];
  for (let i = 1; i < lastCompletedTrace.length; i += 1) {
    const prev = lastCompletedTrace[i - 1];
    const next = lastCompletedTrace[i];
    if (timeMs > next.t) continue;
    const span = Math.max(1, next.t - prev.t);
    const ratio = (timeMs - prev.t) / span;
    return {
      x: prev.x + (next.x - prev.x) * ratio,
      y: prev.y + (next.y - prev.y) * ratio,
      dir: Number.isFinite(prev.dir) ? prev.dir : 0,
    };
  }
  return lastCompletedTrace[lastCompletedTrace.length - 1];
}

function getReplayPulseEventAt(timeMs) {
  if (lastCompletedPulseEvents.length === 0) return null;
  let latest = null;
  for (const event of lastCompletedPulseEvents) {
    if (event.t > timeMs) break;
    latest = event;
  }
  if (!latest) return null;
  if (timeMs - latest.t > 190) return null;
  return latest;
}

function enableControls() {
  retryMapButton.disabled = false;
  newMazeButton.disabled = false;
  replayButton.disabled = runHistory.length === 0;
  toggleMapButton.disabled = demoRoundActive;
  mazeSizeSelect.disabled = false;
  intervalSlider.disabled = true;
  facingSlider.disabled = false;
  runReplaySelect.disabled = runHistory.length === 0;
}

function updateIntervalLabel() {
  intervalValue.textContent = "Continuous Loop";
}

function updateMapVisibility() {
  if (demoRoundActive) {
    mapVisible = true;
  }
  vizSection.hidden = !mapVisible;
  if (demoRoundActive) {
    toggleMapButton.textContent = "Map Locked (Demo)";
  } else {
    toggleMapButton.textContent = mapVisible ? "Hide Map" : "Show Map";
  }
}

function resetPlayerForRun() {
  stopReplay();
  player = { x: 1.5, y: 1.5 };
  goal = { x: mazeSize - 1.5, y: mazeSize - 1.5 };
  guide = { x: 1.5, y: 1.5 };
  mazeCompleted = false;
  runActive = false;
  updateGuideState();
  drawMaze();
  resetCurrentTimerDisplay();
}

function startGameplayNow() {
  facingDegrees = clampAngle(Math.round(facingDegrees / 90) * 90);
  facingSlider.value = String(facingDegrees);
  updateFacingLabel();
  updateListener();
  runActive = true;
  startRunTimer();
  updateGuideState();
  pulseGuide();
  resumeAudioContextSync();
  if (continuousGuideElement) {
    continuousGuideElement.play().catch(() => {});
  }
}

function loadNewMap() {
  stopReplay();
  maze = createMaze(mazeSize, mazeSize);
  mazeSnapshot = cloneMaze(maze);
  currentMapId += 1;
  sameMapTotalMs = 0;
  resetPlayerForRun();
  startGameplayNow();
}

function retrySameMap() {
  stopReplay();
  if (completedRunMs > 0) {
    sameMapTotalMs += completedRunMs;
  }
  maze = cloneMaze(mazeSnapshot);
  resetPlayerForRun();
  startGameplayNow();
}

function startReplay() {
  const selectedRun = getSelectedRunForReplay();
  if (!selectedRun || selectedRun.trace.length < 2) return;
  stopReplay();
  lastCompletedTrace = selectedRun.trace.map((point) => ({ ...point }));
  lastCompletedTraceDurationMs = selectedRun.durationMs;
  lastCompletedPulseEvents = selectedRun.pulseEvents.map((event) => ({ ...event }));
  mapVisible = true;
  updateMapVisibility();
  replayActive = true;
  replayCursorMs = 0;
  drawMaze();
  replayTimerId = setInterval(() => {
    replayCursorMs += 33;
    if (replayCursorMs >= lastCompletedTraceDurationMs) {
      replayCursorMs = lastCompletedTraceDurationMs;
      drawMaze();
      stopReplay();
      drawMaze();
      return;
    }
    drawMaze();
  }, 33);
}

function playOneShotToDestination(buffer, gainValue = 0.9) {
  return new Promise((resolve) => {
    if (!audioCtx || !buffer) {
      resolve();
      return;
    }
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    const gain = audioCtx.createGain();
    gain.gain.value = gainValue;
    source.connect(gain);
    gain.connect(audioCtx.destination);
    source.onended = () => resolve();
    source.start();
  });
}

function playStartBeep() {
  return new Promise((resolve) => {
    if (!audioCtx) {
      resolve();
      return;
    }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    const now = audioCtx.currentTime;
    osc.type = "sine";
    osc.frequency.value = 880;
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.18, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.16);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(now);
    osc.stop(now + 0.18);
    setTimeout(resolve, 190);
  });
}

function waitMs(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function showDemoRoundInstructions() {
  if (demoRoundCompleted) return;
  alert(
    "Demo Round (Map Visible)\n\n" +
      "1) Move with W / A / S / D.\n" +
      "2) Rotate with Left / Right arrows.\n" +
      "3) Follow the voice and also watch the map this round.\n" +
      "4) Orange marker/sound is your guide; green is the goal.\n\n" +
      "After this demo clears, the real game starts with map hidden by default."
  );
}

async function beginRealGameAfterDemo() {
  if (demoTransitionPending || !demoRoundActive) return;
  demoTransitionPending = true;
  await waitMs(260);
  alert(
    "Now the real game begins.\n\n" +
      "The map is now hidden by default.\n" +
      "Use audio direction first.\n" +
      "Open Controls any time to show map, change settings, or replay runs."
  );
  // Alert may suspend the AudioContext; resume it before playing more audio.
  if (audioCtx && audioCtx.state === "suspended") await audioCtx.resume();
  resumeAudioContextSync();
  if (continuousGuideElement) {
    continuousGuideElement.play().catch(() => {});
  }

  demoRoundActive = false;
  demoRoundCompleted = true;
  mapVisible = false;
  updateMapVisibility();
  enableControls();

  stopReplay();
  maze = createMaze(mazeSize, mazeSize);
  mazeSnapshot = cloneMaze(maze);
  currentMapId += 1;
  sameMapTotalMs = 0;
  resetPlayerForRun();
  await playGuideArrivalSequence();
  await playStartBeep();

  if (audioCtx?.state === "suspended") await audioCtx.resume();
  resumeAudioContextSync();
  if (continuousGuideElement) {
    continuousGuideElement.play().catch(() => {});
  }

  startGameplayNow();
  demoTransitionPending = false;
}

function createSpatialPannerAt(worldX, worldY) {
  const localPanner = audioCtx.createPanner();
  localPanner.panningModel = "equalpower";
  localPanner.distanceModel = "inverse";
  localPanner.refDistance = 0.9;
  localPanner.maxDistance = 24;
  localPanner.rolloffFactor = 1.25;
  localPanner.coneInnerAngle = 360;
  localPanner.coneOuterAngle = 360;
  localPanner.coneOuterGain = 0;
  localPanner.positionX.setValueAtTime(worldX - player.x, audioCtx.currentTime);
  localPanner.positionY.setValueAtTime(0, audioCtx.currentTime);
  localPanner.positionZ.setValueAtTime(worldY - player.y, audioCtx.currentTime);
  return localPanner;
}

function playGuideFootstepAt(worldX, worldY, gainAmount = 0.08) {
  if (!audioCtx) return;
  const now = audioCtx.currentTime;
  const noiseBuffer = audioCtx.createBuffer(1, Math.floor(audioCtx.sampleRate * 0.06), audioCtx.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < data.length; i += 1) {
    data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
  }
  const source = audioCtx.createBufferSource();
  source.buffer = noiseBuffer;
  const filter = audioCtx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.setValueAtTime(760, now);
  const gain = audioCtx.createGain();
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(gainAmount, now + 0.008);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.1);
  const localPanner = createSpatialPannerAt(worldX, worldY);
  source.connect(filter);
  filter.connect(gain);
  gain.connect(localPanner);
  localPanner.connect(audioCtx.destination);
  source.start(now);
  source.stop(now + 0.11);
}

function playGuideCalloutAt(buffer, worldX, worldY, gainAmount = 0.98) {
  return new Promise((resolve) => {
    if (!audioCtx || !buffer) {
      resolve();
      return;
    }
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    const gain = audioCtx.createGain();
    gain.gain.value = gainAmount;
    const localPanner = createSpatialPannerAt(worldX, worldY);
    source.connect(gain);
    gain.connect(localPanner);
    localPanner.connect(audioCtx.destination);
    source.onended = () => resolve();
    source.start();
  });
}

async function playGuideArrivalSequence() {
  if (!audioCtx || guideClipBuffers.length === 0) return;
  mazeStatusLabel.textContent = "Guide is taking position...";
  await waitMs(420);
  updateGuideWaypoint();
  const targetX = guide.x;
  const targetY = guide.y;
  const startX = player.x + 0.15;
  const startY = player.y + 1.1;
  const steps = 6;
  for (let index = 0; index < steps; index += 1) {
    const ratio = (index + 1) / steps;
    const x = startX + (targetX - startX) * ratio;
    const y = startY + (targetY - startY) * ratio;
    playGuideFootstepAt(x, y, 0.09);
    await waitMs(190);
  }
  await waitMs(170);
  const clip = guideClipBuffers[guideClipIndex];
  guideClipIndex = (guideClipIndex + 1) % guideClipBuffers.length;
  await playGuideCalloutAt(clip, targetX, targetY, 1.02);
}

onboardingLanguage?.addEventListener("change", () => {
  renderOnboarding(onboardingLanguage.value);
  if (voiceSelect) {
    voiceSelect.value = onboardingLanguage.value === "ja" ? "japanese" : "chinese";
    voiceSelect.dispatchEvent(new Event("change"));
  }
});

enterGameButton?.addEventListener("click", () => {
  if (onboardingScreen) onboardingScreen.hidden = true;
  if (gamePanel) gamePanel.hidden = false;
  startButton.focus();
});

startButton.addEventListener("click", async () => {
  // ── SYNCHRONOUS BLOCK ──────────────────────────────────────────────────────
  // Everything here runs in the same browser gesture frame so autoplay is
  // guaranteed.  We must NOT await or call alert() before reaching the end of
  // this block.
  if (!audioCtx) {
    audioCtx = new AudioContext();
    toneFilter = audioCtx.createBiquadFilter();
    toneFilter.type = "lowpass";
    toneFilter.frequency.value = 5200;
    toneFilter.Q.value = 0.35;
    distanceToneGain = audioCtx.createGain();
    distanceToneGain.gain.value = 1;
    panner = audioCtx.createPanner();
    // "equalpower" is more reliable across browsers/OSes than "HRTF" (which
    // can output silence with some sink configurations).
    panner.panningModel = "equalpower";
    panner.distanceModel = "inverse";
    panner.refDistance = 0.9;
    panner.maxDistance = 24;
    panner.rolloffFactor = 1.3;
    panner.coneInnerAngle = 360;
    // Some engines behave badly with coneOuterAngle 0; keep a full sphere.
    panner.coneOuterAngle = 360;
    panner.coneOuterGain = 0;
    toneFilter.connect(distanceToneGain);
    distanceToneGain.connect(panner);
    panner.connect(audioCtx.destination);
    updateListener();
  }
  if (!continuousGuideMediaNode) {
    if (!continuousGuideElement) {
      continuousGuideElement = new Audio(getContinuousGuideTrack());
      continuousGuideElement.loop = true;
      continuousGuideElement.preload = "auto";
      continuousGuideElement.volume = 1;
    }
    continuousGuideMediaNode = audioCtx.createMediaElementSource(continuousGuideElement);
    continuousGuideGain = audioCtx.createGain();
    continuousGuideGain.gain.value = 0.0001;
    continuousGuideMediaNode.connect(continuousGuideGain);
    continuousGuideGain.connect(toneFilter);
  }
  // AudioContext starts "suspended"; resume must run in the *same* synchronous
  // turn as the click/tap (before await), or Safari/Firefox may never process
  // MediaElementSourceNode output even though play() succeeded.
  resumeAudioContextSync();
  if (continuousGuideElement) {
    continuousGuideElement.play().catch(() => {});
  }
  resumeAudioContextSync();
  // ── END SYNCHRONOUS BLOCK ──────────────────────────────────────────────────

  if (!safetyPromptShown) {
    alert("For real play: close your eyes or wear a blindfold and use audio only.");
    safetyPromptShown = true;
  }
  if (audioCtx.state === "suspended") await audioCtx.resume();

  // Load short voice clips (intro, guide callouts).  The continuous track is
  // already wired up above so loadGuideClipBuffer only needs to decode the
  // short buffers now.
  await loadGuideClipBuffer();

  startButton.disabled = true;
  startButton.textContent = "Tutorial...";
  maze = createMaze(mazeSize, mazeSize);
  mazeSnapshot = cloneMaze(maze);
  sameMapTotalMs = 0;
  currentMapId = 1;
  runHistory = [];
  runHistoryCounter = 1;
  updateReplaySelectOptions();
  demoRoundActive = true;
  demoRoundCompleted = false;
  demoTransitionPending = false;
  mapVisible = true;
  updateMapVisibility();
  showDemoRoundInstructions();
  // Resume in case the alert above suspended the context.
  if (audioCtx.state === "suspended") await audioCtx.resume();
  resetPlayerForRun();
  updateTimerHud();

  mazeStatusLabel.textContent = "Tutorial in progress";
  await playOneShotToDestination(introClipBuffer, 0.92);
  await playGuideArrivalSequence();
  await playStartBeep();

  if (audioCtx?.state === "suspended") await audioCtx.resume();
  resumeAudioContextSync();
  if (continuousGuideElement) {
    continuousGuideElement.play().catch(() => {});
  }

  startGameplayNow();
  enableControls();
  startButton.textContent = "Audio Running";
});

mazeSizeSelect.addEventListener("change", () => {
  const selected = Number(mazeSizeSelect.value);
  if (!Number.isFinite(selected) || selected < 9) return;
  mazeSize = selected;
  if (startButton.disabled) {
    loadNewMap();
  } else {
    maze = createMaze(mazeSize, mazeSize);
    mazeSnapshot = cloneMaze(maze);
    resetPlayerForRun();
    mazeStatusLabel.textContent = "Waiting to start";
    updateTimerHud();
  }
});

voiceSelect.addEventListener("change", async () => {
  if (onboardingLanguage) {
    onboardingLanguage.value = voiceSelect.value === "japanese" ? "ja" : "zh";
    renderOnboarding(onboardingLanguage.value);
  }
  if (!audioCtx) return;
  await loadGuideClipBuffer(true);
  if (guideClipBuffers.length === 0) {
    mazeStatusLabel.textContent = "Could not load selected guide voice";
    return;
  }
  const track = getContinuousGuideTrack();
  const tail = track.replace("./", "");
  if (
    continuousGuideElement &&
    typeof continuousGuideElement.src === "string" &&
    !continuousGuideElement.src.endsWith(tail)
  ) {
    const wasPlaying = runActive && !mazeCompleted;
    stopContinuousGuideVoice();
    continuousGuideElement.src = track;
    continuousGuideElement.load();
    if (wasPlaying) {
      resumeAudioContextSync();
      continuousGuideElement.play().catch(() => {});
      ensureContinuousGuideVoice();
    }
  }
});

retryMapButton.addEventListener("click", () => {
  retrySameMap();
});

newMazeButton.addEventListener("click", () => {
  loadNewMap();
});

replayButton.addEventListener("click", () => {
  startReplay();
});

runReplaySelect.addEventListener("change", () => {
  replayButton.disabled = !getSelectedRunForReplay();
});

toggleMapButton.addEventListener("click", () => {
  if (demoRoundActive) return;
  mapVisible = !mapVisible;
  updateMapVisibility();
});

intervalSlider.addEventListener("input", (event) => {
  pulseIntervalMs = Math.round(Number(event.target.value) * 1000);
  updateIntervalLabel();
  if (!facingSlider.disabled) updatePulseLoop();
});

facingSlider.addEventListener("input", (event) => {
  facingDegrees = clampAngle(Math.round(Number(event.target.value) / 90) * 90);
  facingSlider.value = String(facingDegrees);
  updateFacingLabel();
  updateListener();
  updateGuideState();
  drawMaze();
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !startButton.disabled && !event.repeat && !gamePanel.hidden) {
    event.preventDefault();
    startButton.click();
    return;
  }
  if (facingSlider.disabled) return;
  if (replayActive) return;
  if (!runActive) return;
  if (event.repeat) return;
  const key = event.key.toLowerCase();
  if (key === "w") {
    event.preventDefault();
    movePlayer(0, -1);
  } else if (key === "s") {
    event.preventDefault();
    movePlayer(0, 1);
  } else if (key === "a") {
    event.preventDefault();
    movePlayer(-1, 0);
  } else if (key === "d") {
    event.preventDefault();
    movePlayer(1, 0);
  } else if (event.key === "ArrowLeft") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees - 90);
    facingSlider.value = String(facingDegrees);
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  } else if (event.key === "ArrowRight") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees + 90);
    facingSlider.value = String(facingDegrees);
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  }
});

window.addEventListener("beforeunload", () => {
  if (pulseTimerId) clearInterval(pulseTimerId);
  if (runTickerId) clearInterval(runTickerId);
  if (replayTimerId) clearInterval(replayTimerId);
  stopContinuousGuideVoice();
  if (audioCtx) audioCtx.close();
});

mazeSize = Number(mazeSizeSelect.value) || DEFAULT_MAZE_SIZE;
maze = createMaze(mazeSize, mazeSize);
mazeSnapshot = cloneMaze(maze);
renderOnboarding(onboardingLanguage?.value || "zh");
updateIntervalLabel();
updateMapVisibility();
updateFacingLabel();
updateTimerHud();
updateReplaySelectOptions();
drawMaze();
/*
const startButton = document.getElementById("startButton");
const newMazeButton = document.getElementById("newMazeButton");
const toggleMapButton = document.getElementById("toggleMapButton");
const intervalSlider = document.getElementById("intervalSlider");
const intervalValue = document.getElementById("intervalValue");
const facingSlider = document.getElementById("facingSlider");
const facingLabel = document.getElementById("facingLabel");
const guideDirectionLabel = document.getElementById("guideDirectionLabel");
const distanceLabel = document.getElementById("distanceLabel");
const mazeStatusLabel = document.getElementById("mazeStatusLabel");
const vizSection = document.getElementById("vizSection");
const canvas = document.getElementById("topDownCanvas");
const ctx = canvas.getContext("2d");

const MAZE_WIDTH = 13;
const MAZE_HEIGHT = 13;
const MOVE_STEP = 0.22;
const PLAYER_RADIUS = 0.16;
const WALL_THICKNESS = 0.13;

const CARDINAL_LABELS = ["North", "East", "South", "West"];
const GUIDE_CLIP_URLS = [
  "./generated_game_voice_lines/bright_adventurer_01_this_way.wav",
  "./generated_game_voice_lines/bright_adventurer_01_over_here.wav",
  "./generated_game_voice_lines/bright_adventurer_01_come_here.wav",
  "./generated_game_voice_lines/bright_adventurer_04_quickly_lets_go.wav",
];

let audioCtx = null;
let toneFilter = null;
let distanceToneGain = null;
let panner = null;
let guideClipBuffers = [];
let guideClipIndex = 0;
let pulseTimerId = null;
let activePulseIntervalMs = null;
let pulsePeak = 0.3;
let pulseIntervalMs = 2400;

let facingDegrees = 0;
let maze = [];
let player = { x: 1.5, y: 1.5 };
let goal = { x: MAZE_WIDTH - 1.5, y: MAZE_HEIGHT - 1.5 };
let guide = { x: 1.5, y: 1.5 };
let mazeCompleted = false;
let mapVisible = false;

function clampAngle(value) {
  const normalized = value % 360;
  return normalized < 0 ? normalized + 360 : normalized;
}

function distance2d(ax, ay, bx, by) {
  const dx = ax - bx;
  const dy = ay - by;
  return Math.sqrt(dx * dx + dy * dy);
}

function createMaze(width, height) {
  const grid = Array.from({ length: height }, () => Array(width).fill(1));

  function shuffle(values) {
    const copy = [...values];
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function carve(x, y) {
    grid[y][x] = 0;
    const dirs = shuffle([
      [2, 0],
      [-2, 0],
      [0, 2],
      [0, -2],
    ]);
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx <= 0 || ny <= 0 || nx >= width - 1 || ny >= height - 1) continue;
      if (grid[ny][nx] !== 1) continue;
      grid[y + dy / 2][x + dx / 2] = 0;
      carve(nx, ny);
    }
  }

  carve(1, 1);
  grid[1][1] = 0;
  grid[height - 2][width - 2] = 0;
  return grid;
}

function isWallAt(x, y) {
  const gridX = Math.floor(x);
  const gridY = Math.floor(y);
  if (gridX < 0 || gridY < 0 || gridX >= MAZE_WIDTH || gridY >= MAZE_HEIGHT) return true;
  return maze[gridY][gridX] === 1;
}

function canMoveTo(x, y) {
  return (
    !isWallAt(x - PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x - PLAYER_RADIUS, y + PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y + PLAYER_RADIUS)
  );
}

function getPlayerCell() {
  return { x: Math.floor(player.x), y: Math.floor(player.y) };
}

function getGoalCell() {
  return { x: Math.floor(goal.x), y: Math.floor(goal.y) };
}

function getCellKey(x, y) {
  return `${x},${y}`;
}

function computePathBfs(startCell, endCell) {
  const queue = [startCell];
  const visited = new Set([getCellKey(startCell.x, startCell.y)]);
  const parent = new Map();
  const moves = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
  ];

  while (queue.length) {
    const current = queue.shift();
    if (current.x === endCell.x && current.y === endCell.y) break;
    for (const [dx, dy] of moves) {
      const nx = current.x + dx;
      const ny = current.y + dy;
      if (nx < 0 || ny < 0 || nx >= MAZE_WIDTH || ny >= MAZE_HEIGHT) continue;
      if (maze[ny][nx] === 1) continue;
      const key = getCellKey(nx, ny);
      if (visited.has(key)) continue;
      visited.add(key);
      parent.set(key, current);
      queue.push({ x: nx, y: ny });
    }
  }

  const endKey = getCellKey(endCell.x, endCell.y);
  if (!visited.has(endKey)) return [];

  const path = [];
  let current = endCell;
  while (current) {
    path.push(current);
    current = parent.get(getCellKey(current.x, current.y)) || null;
  }
  path.reverse();
  return path;
}

function chooseGuideCellFromPath(path) {
  if (path.length <= 1) return path[0] || getGoalCell();
  if (path.length === 2) return path[1];
  const initialDx = path[1].x - path[0].x;
  const initialDy = path[1].y - path[0].y;
  let index = 1;
  while (index + 1 < path.length) {
    const nextDx = path[index + 1].x - path[index].x;
    const nextDy = path[index + 1].y - path[index].y;
    if (nextDx !== initialDx || nextDy !== initialDy) return path[index];
    index += 1;
  }
  return path[path.length - 1];
}

function updateGuideWaypoint() {
  const path = computePathBfs(getPlayerCell(), getGoalCell());
  const waypointCell = chooseGuideCellFromPath(path);
  guide = { x: waypointCell.x + 0.5, y: waypointCell.y + 0.5 };
}

function getDistanceToGoal() {
  return distance2d(player.x, player.y, goal.x, goal.y);
}

function getDistanceToGuide() {
  return distance2d(player.x, player.y, guide.x, guide.y);
}

function getRelativeDirectionLabel() {
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const rightX = Math.cos(facingRad);
  const rightY = Math.sin(facingRad);
  const forwardComponent = toGuideX * forwardX + toGuideY * forwardY;
  const rightComponent = toGuideX * rightX + toGuideY * rightY;
  const relative = Math.atan2(rightComponent, forwardComponent);
  const sector = Math.round(relative / (Math.PI / 4));
  const labels = [
    "Forward",
    "Forward-Right",
    "Right",
    "Back-Right",
    "Back",
    "Back-Left",
    "Left",
    "Forward-Left",
  ];
  return labels[((sector % 8) + 8) % 8];
}

function updateFacingLabel() {
  const cardinalIndex = Math.round(facingDegrees / 90) % 4;
  facingLabel.textContent = `${Math.round(facingDegrees)}° (${CARDINAL_LABELS[cardinalIndex]})`;
}

function updateGuideAudio() {
  if (!audioCtx || !panner || !distanceToneGain || !toneFilter || mazeCompleted) return;
  const now = audioCtx.currentTime;
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const distance = getDistanceToGuide();
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const frontness = Math.max(
    -1,
    Math.min(1, (toGuideX * forwardX + toGuideY * forwardY) / Math.max(distance, 0.001))
  );

  panner.positionX.setValueAtTime(toGuideX, now);
  panner.positionY.setValueAtTime(0, now);
  panner.positionZ.setValueAtTime(toGuideY, now);

  const distanceFactor = Math.max(0.6, Math.min(1.1, 1.18 - distance * 0.045));
  const nearBoost = Math.max(0, Math.min(0.42, (2.6 - distance) * 0.18));
  const frontScale = (frontness + 1) / 2;
  const directionalGain = 0.62 + frontScale * 0.38;
  distanceToneGain.gain.setTargetAtTime((distanceFactor + nearBoost) * directionalGain, now, 0.04);
  toneFilter.frequency.setTargetAtTime(1800, now, 0.08);
  pulsePeak = 0.32;
}

function updateListener() {
  if (!audioCtx) return;
  const listener = audioCtx.listener;
  const rad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(rad);
  const forwardZ = -Math.cos(rad);
  if (listener.positionX) {
    listener.positionX.setValueAtTime(0, audioCtx.currentTime);
    listener.positionY.setValueAtTime(0, audioCtx.currentTime);
    listener.positionZ.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardX.setValueAtTime(forwardX, audioCtx.currentTime);
    listener.forwardY.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardZ.setValueAtTime(forwardZ, audioCtx.currentTime);
    listener.upX.setValueAtTime(0, audioCtx.currentTime);
    listener.upY.setValueAtTime(1, audioCtx.currentTime);
    listener.upZ.setValueAtTime(0, audioCtx.currentTime);
  } else if (listener.setOrientation) {
    listener.setPosition(0, 0, 0);
    listener.setOrientation(forwardX, 0, forwardZ, 0, 1, 0);
  }
}

function pulseGuide() {
  if (!audioCtx || !distanceToneGain || !toneFilter || guideClipBuffers.length === 0 || mazeCompleted) {
    return;
  }
  const now = audioCtx.currentTime;
  const clipBuffer = guideClipBuffers[guideClipIndex];
  guideClipIndex = (guideClipIndex + 1) % guideClipBuffers.length;
  const source = audioCtx.createBufferSource();
  source.buffer = clipBuffer;
  source.playbackRate.value = 1;
  const pulseGain = audioCtx.createGain();
  pulseGain.gain.setValueAtTime(0.0001, now);
  pulseGain.gain.exponentialRampToValueAtTime(pulsePeak, now + 0.02);
  const clipDuration = Math.min(clipBuffer.duration, Math.max(1.8, pulseIntervalMs / 1000 - 0.15));
  const fadeOutStart = Math.max(now + 0.3, now + clipDuration - 0.16);
  pulseGain.gain.setValueAtTime(pulsePeak, fadeOutStart);
  pulseGain.gain.exponentialRampToValueAtTime(0.0001, now + clipDuration);
  source.connect(pulseGain);
  pulseGain.connect(toneFilter);
  source.start(now);
  source.stop(now + clipDuration);
}

function updatePulseLoop() {
  if (mazeCompleted) {
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
      activePulseIntervalMs = null;
    }
    return;
  }
  if (pulseTimerId && activePulseIntervalMs === pulseIntervalMs) return;
  if (pulseTimerId) clearInterval(pulseTimerId);
  pulseTimerId = setInterval(pulseGuide, pulseIntervalMs);
  activePulseIntervalMs = pulseIntervalMs;
}

function updateGuideState() {
  updateGuideWaypoint();
  guideDirectionLabel.textContent = getRelativeDirectionLabel();
  distanceLabel.textContent = `${getDistanceToGuide().toFixed(1)} cells`;
  mazeStatusLabel.textContent = mazeCompleted ? "Goal reached" : "Follow the guide";
  updateGuideAudio();
  updatePulseLoop();
}

function checkGoal() {
  if (mazeCompleted) return;
  if (getDistanceToGoal() <= 0.5) {
    mazeCompleted = true;
    mazeStatusLabel.textContent = "Goal reached";
    guideDirectionLabel.textContent = "Done";
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
    }
  }
}

function movePlayer(localX, localY) {
  if (mazeCompleted) return;
  const rad = (facingDegrees * Math.PI) / 180;
  const worldX = localX * Math.cos(rad) - localY * Math.sin(rad);
  const worldY = localX * Math.sin(rad) + localY * Math.cos(rad);
  const nextX = player.x + worldX * MOVE_STEP;
  const nextY = player.y + worldY * MOVE_STEP;

  let finalX = player.x;
  let finalY = player.y;
  if (canMoveTo(nextX, player.y)) finalX = nextX;
  if (canMoveTo(finalX, nextY)) finalY = nextY;
  player.x = Math.min(MAZE_WIDTH - 1.01, Math.max(1.01, finalX));
  player.y = Math.min(MAZE_HEIGHT - 1.01, Math.max(1.01, finalY));

  checkGoal();
  updateGuideState();
  drawMaze();
}

async function loadGuideClipBuffer() {
  if (!audioCtx || guideClipBuffers.length > 0) return;
  for (const url of GUIDE_CLIP_URLS) {
    try {
      const response = await fetch(url);
      if (!response.ok) continue;
      const decoded = await audioCtx.decodeAudioData(await response.arrayBuffer());
      guideClipBuffers.push(decoded);
    } catch {
      // Try next clip.
    }
  }
}

async function initializeAudio() {
  if (audioCtx) return;
  audioCtx = new AudioContext();
  toneFilter = audioCtx.createBiquadFilter();
  distanceToneGain = audioCtx.createGain();
  panner = audioCtx.createPanner();
  toneFilter.type = "lowpass";
  toneFilter.frequency.value = 2400;
  toneFilter.Q.value = 0.5;
  distanceToneGain.gain.value = 1;
  panner.panningModel = "HRTF";
  panner.distanceModel = "inverse";
  panner.refDistance = 0.9;
  panner.maxDistance = 24;
  panner.rolloffFactor = 1.3;
  panner.coneInnerAngle = 360;
  panner.coneOuterAngle = 0;
  panner.coneOuterGain = 0;
  toneFilter.connect(distanceToneGain);
  distanceToneGain.connect(panner);
  panner.connect(audioCtx.destination);

  await loadGuideClipBuffer();
  if (guideClipBuffers.length === 0) mazeStatusLabel.textContent = "Could not load guide clip";
  updateListener();
  updateGuideState();
  pulseGuide();
}

function regenerateMaze() {
  maze = createMaze(MAZE_WIDTH, MAZE_HEIGHT);
  player = { x: 1.5, y: 1.5 };
  goal = { x: MAZE_WIDTH - 1.5, y: MAZE_HEIGHT - 1.5 };
  guide = { x: 1.5, y: 1.5 };
  mazeCompleted = false;
  updateGuideState();
  drawMaze();
}

function drawMaze() {
  const width = canvas.width;
  const height = canvas.height;
  const cellW = width / MAZE_WIDTH;
  const cellH = height / MAZE_HEIGHT;
  const wallInset = Math.min(cellW, cellH) * WALL_THICKNESS;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, width, height);
  for (let y = 0; y < MAZE_HEIGHT; y += 1) {
    for (let x = 0; x < MAZE_WIDTH; x += 1) {
      if (maze[y]?.[x] !== 1) continue;
      ctx.fillStyle = "#1f1f1f";
      ctx.fillRect(
        x * cellW + wallInset,
        y * cellH + wallInset,
        cellW - wallInset * 2,
        cellH - wallInset * 2
      );
    }
  }
  const goalX = goal.x * cellW;
  const goalY = goal.y * cellH;
  const guideX = guide.x * cellW;
  const guideY = guide.y * cellH;
  ctx.fillStyle = mazeCompleted ? "#8ae68a" : "#10b981";
  ctx.beginPath();
  ctx.arc(goalX, goalY, Math.min(cellW, cellH) * 0.22, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#f97316";
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.28, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "#f97316";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.48, 0, Math.PI * 2);
  ctx.stroke();

  const px = player.x * cellW;
  const py = player.y * cellH;
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(px, py, Math.min(cellW, cellH) * 0.24, 0, Math.PI * 2);
  ctx.fill();
  const rad = (facingDegrees * Math.PI) / 180;
  const arrowLength = Math.min(cellW, cellH) * 0.7;
  ctx.strokeStyle = "#e5e5e5";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(px, py);
  ctx.lineTo(px + Math.sin(rad) * arrowLength, py - Math.cos(rad) * arrowLength);
  ctx.stroke();
  ctx.fillStyle = "#f3f4f6";
  ctx.font = "12px Arial";
  ctx.fillText("Guide Sound", guideX + 8, guideY - 8);
  ctx.fillText("Goal", goalX + 8, goalY + 14);
}

function enableControls() {
  newMazeButton.disabled = false;
  toggleMapButton.disabled = false;
  intervalSlider.disabled = false;
  facingSlider.disabled = false;
}

function updateIntervalLabel() {
  intervalValue.textContent = `${(pulseIntervalMs / 1000).toFixed(1)}s`;
}

function updateMapVisibility() {
  vizSection.hidden = !mapVisible;
  toggleMapButton.textContent = mapVisible ? "Hide Map" : "Show Map";
}

startButton.addEventListener("click", async () => {
  await initializeAudio();
  if (audioCtx.state === "suspended") await audioCtx.resume();
  enableControls();
  startButton.disabled = true;
  startButton.textContent = "Audio Running";
  regenerateMaze();
});

newMazeButton.addEventListener("click", () => {
  regenerateMaze();
});

toggleMapButton.addEventListener("click", () => {
  mapVisible = !mapVisible;
  updateMapVisibility();
});

intervalSlider.addEventListener("input", (event) => {
  pulseIntervalMs = Math.round(Number(event.target.value) * 1000);
  updateIntervalLabel();
  if (!facingSlider.disabled) updatePulseLoop();
});

facingSlider.addEventListener("input", (event) => {
  facingDegrees = clampAngle(Number(event.target.value));
  updateFacingLabel();
  updateListener();
  updateGuideState();
  drawMaze();
});

window.addEventListener("keydown", (event) => {
  if (facingSlider.disabled) return;
  const key = event.key.toLowerCase();
  if (key === "w") {
    event.preventDefault();
    movePlayer(0, -1);
  } else if (key === "s") {
    event.preventDefault();
    movePlayer(0, 1);
  } else if (key === "a") {
    event.preventDefault();
    movePlayer(-1, 0);
  } else if (key === "d") {
    event.preventDefault();
    movePlayer(1, 0);
  } else if (event.key === "ArrowLeft") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees - 15);
    facingSlider.value = String(Math.round(facingDegrees));
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  } else if (event.key === "ArrowRight") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees + 15);
    facingSlider.value = String(Math.round(facingDegrees));
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  }
});

window.addEventListener("beforeunload", () => {
  if (pulseTimerId) clearInterval(pulseTimerId);
  if (audioCtx) audioCtx.close();
});

maze = createMaze(MAZE_WIDTH, MAZE_HEIGHT);
updateIntervalLabel();
updateMapVisibility();
updateFacingLabel();
drawMaze();
/*
const startButton = document.getElementById("startButton");
const newMazeButton = document.getElementById("newMazeButton");
const intervalSlider = document.getElementById("intervalSlider");
const intervalValue = document.getElementById("intervalValue");
const facingSlider = document.getElementById("facingSlider");
const facingLabel = document.getElementById("facingLabel");
const guideDirectionLabel = document.getElementById("guideDirectionLabel");
const distanceLabel = document.getElementById("distanceLabel");
const crouchLabel = document.getElementById("crouchLabel");
const mazeStatusLabel = document.getElementById("mazeStatusLabel");
const canvas = document.getElementById("topDownCanvas");
const ctx = canvas.getContext("2d");

const MAZE_WIDTH = 13;
const MAZE_HEIGHT = 13;
const MOVE_STEP = 0.22;
const PLAYER_RADIUS = 0.16;
const WALL_THICKNESS = 0.13;

const CARDINAL_LABELS = ["North", "East", "South", "West"];
const GUIDE_CLIP_URLS = [
  "./generated_game_voice_lines/bright_adventurer_01_this_way.wav",
  "./generated_game_voice_lines/bright_adventurer_01_over_here.wav",
  "./generated_game_voice_lines/bright_adventurer_01_come_here.wav",
  "./generated_game_voice_lines/bright_adventurer_04_quickly_lets_go.wav",
];
const JUMP_CLIP_URLS = {
  jump: "./generated_game_voice_lines/bright_adventurer_02_jump.wav",
  watchOut: "./generated_game_voice_lines/bright_adventurer_02_watch_out_jump.wav",
};

let audioCtx = null;
let toneFilter = null;
let distanceToneGain = null;
let panner = null;
let guideClipBuffers = [];
let guideClipIndex = 0;
let jumpClipBuffers = { jump: null, watchOut: null };
let pulseTimerId = null;
let activePulseIntervalMs = null;
let pulsePeak = 0.3;
let pulseIntervalMs = 2400;

let facingDegrees = 0;
let maze = [];
let player = { x: 1.5, y: 1.5 };
let goal = { x: MAZE_WIDTH - 1.5, y: MAZE_HEIGHT - 1.5 };
let guide = { x: 1.5, y: 1.5 };
let mazeCompleted = false;

let jumpObstacles = [];
let jumpActiveUntilMs = 0;
let lastJumpPromptAtMs = 0;
let lastWatchOutPromptAtMs = 0;

function clampAngle(value) {
  const normalized = value % 360;
  return normalized < 0 ? normalized + 360 : normalized;
}

function nowMs() {
  return Date.now();
}

function isJumpActive() {
  return nowMs() <= jumpActiveUntilMs;
}

function updateJumpLabel() {
  crouchLabel.textContent = isJumpActive() ? "Jumping" : "Ready";
}

function createMaze(width, height) {
  const grid = Array.from({ length: height }, () => Array(width).fill(1));
  function shuffle(values) {
    const copy = [...values];
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }
  function carve(x, y) {
    grid[y][x] = 0;
    const dirs = shuffle([
      [2, 0],
      [-2, 0],
      [0, 2],
      [0, -2],
    ]);
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx <= 0 || ny <= 0 || nx >= width - 1 || ny >= height - 1) continue;
      if (grid[ny][nx] !== 1) continue;
      grid[y + dy / 2][x + dx / 2] = 0;
      carve(nx, ny);
    }
  }
  carve(1, 1);
  grid[1][1] = 0;
  grid[height - 2][width - 2] = 0;
  return grid;
}

function isWallAt(x, y) {
  const gridX = Math.floor(x);
  const gridY = Math.floor(y);
  if (gridX < 0 || gridY < 0 || gridX >= MAZE_WIDTH || gridY >= MAZE_HEIGHT) return true;
  return maze[gridY][gridX] === 1;
}

function canMoveTo(x, y) {
  return (
    !isWallAt(x - PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x - PLAYER_RADIUS, y + PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y + PLAYER_RADIUS)
  );
}

function distance2d(ax, ay, bx, by) {
  const dx = ax - bx;
  const dy = ay - by;
  return Math.sqrt(dx * dx + dy * dy);
}

function getDistanceToGoal() {
  return distance2d(player.x, player.y, goal.x, goal.y);
}

function getDistanceToGuide() {
  return distance2d(player.x, player.y, guide.x, guide.y);
}

function getPlayerCell() {
  return { x: Math.floor(player.x), y: Math.floor(player.y) };
}

function getGoalCell() {
  return { x: Math.floor(goal.x), y: Math.floor(goal.y) };
}

function getCellKey(x, y) {
  return `${x},${y}`;
}

function computePathBfs(startCell, endCell) {
  const queue = [startCell];
  const visited = new Set([getCellKey(startCell.x, startCell.y)]);
  const parent = new Map();
  const moves = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
  ];
  while (queue.length) {
    const current = queue.shift();
    if (current.x === endCell.x && current.y === endCell.y) break;
    for (const [dx, dy] of moves) {
      const nx = current.x + dx;
      const ny = current.y + dy;
      if (nx < 0 || ny < 0 || nx >= MAZE_WIDTH || ny >= MAZE_HEIGHT) continue;
      if (maze[ny][nx] === 1) continue;
      const key = getCellKey(nx, ny);
      if (visited.has(key)) continue;
      visited.add(key);
      parent.set(key, current);
      queue.push({ x: nx, y: ny });
    }
  }
  const endKey = getCellKey(endCell.x, endCell.y);
  if (!visited.has(endKey)) return [];
  const path = [];
  let current = endCell;
  while (current) {
    path.push(current);
    current = parent.get(getCellKey(current.x, current.y)) || null;
  }
  path.reverse();
  return path;
}

function chooseGuideCellFromPath(path) {
  if (path.length <= 1) return path[0] || getGoalCell();
  if (path.length === 2) return path[1];
  const initialDx = path[1].x - path[0].x;
  const initialDy = path[1].y - path[0].y;
  let index = 1;
  while (index + 1 < path.length) {
    const nextDx = path[index + 1].x - path[index].x;
    const nextDy = path[index + 1].y - path[index].y;
    if (nextDx !== initialDx || nextDy !== initialDy) return path[index];
    index += 1;
  }
  return path[path.length - 1];
}

function updateGuideWaypoint() {
  const path = computePathBfs(getPlayerCell(), getGoalCell());
  const waypointCell = chooseGuideCellFromPath(path);
  guide = { x: waypointCell.x + 0.5, y: waypointCell.y + 0.5 };
}

function generateJumpObstacles() {
  const path = computePathBfs({ x: 1, y: 1 }, getGoalCell());
  jumpObstacles = [];
  if (path.length < 8) return;

  const count = Math.min(3, Math.max(1, Math.floor(path.length / 9)));
  const segment = Math.floor(path.length / (count + 1));
  for (let i = 1; i <= count; i += 1) {
    const jitter = Math.floor(Math.random() * 3) - 1;
    const idx = Math.max(2, Math.min(path.length - 3, i * segment + jitter));
    const cell = path[idx];
    if (cell.x === 1 && cell.y === 1) continue;
    if (cell.x === Math.floor(goal.x) && cell.y === Math.floor(goal.y)) continue;
    jumpObstacles.push({ x: cell.x + 0.5, y: cell.y + 0.5, cleared: false });
  }
}

function getBlockingObstacleNear(x, y, radius = 0.34) {
  for (const obstacle of jumpObstacles) {
    if (obstacle.cleared) continue;
    if (distance2d(x, y, obstacle.x, obstacle.y) <= radius) return obstacle;
  }
  return null;
}

function playPrompt(type, force = false) {
  if (!audioCtx || audioCtx.state !== "running") return;
  const buffer = jumpClipBuffers[type];
  if (!buffer) return;
  const now = nowMs();
  if (!force && now - lastJumpPromptAtMs < 2800) return;
  lastJumpPromptAtMs = now;
  const source = audioCtx.createBufferSource();
  source.buffer = buffer;
  const gain = audioCtx.createGain();
  gain.gain.value = 0.92;
  source.connect(gain);
  gain.connect(audioCtx.destination);
  source.start();
}

function maybeWatchOutForObstacle() {
  const now = nowMs();
  if (now - lastWatchOutPromptAtMs < 4000) return;
  for (const obstacle of jumpObstacles) {
    if (obstacle.cleared) continue;
    const d = distance2d(player.x, player.y, obstacle.x, obstacle.y);
    if (d < 2.1) {
      lastWatchOutPromptAtMs = now;
      playPrompt("watchOut", true);
      break;
    }
  }
}

function markClearedObstacles() {
  for (const obstacle of jumpObstacles) {
    if (obstacle.cleared) continue;
    if (distance2d(player.x, player.y, obstacle.x, obstacle.y) < 0.42) {
      obstacle.cleared = true;
    }
  }
}

function movePlayer(localX, localY) {
  if (mazeCompleted) return;
  const rad = (facingDegrees * Math.PI) / 180;
  const worldX = localX * Math.cos(rad) - localY * Math.sin(rad);
  const worldY = localX * Math.sin(rad) + localY * Math.cos(rad);
  const nextX = player.x + worldX * MOVE_STEP;
  const nextY = player.y + worldY * MOVE_STEP;

  const blocker = getBlockingObstacleNear(nextX, nextY);
  if (blocker && !isJumpActive()) {
    mazeStatusLabel.textContent = "Obstacle ahead - press Space to jump";
    playPrompt("jump");
    return;
  }

  let finalX = player.x;
  let finalY = player.y;
  if (canMoveTo(nextX, player.y)) finalX = nextX;
  if (canMoveTo(finalX, nextY)) finalY = nextY;
  player.x = Math.min(MAZE_WIDTH - 1.01, Math.max(1.01, finalX));
  player.y = Math.min(MAZE_HEIGHT - 1.01, Math.max(1.01, finalY));

  markClearedObstacles();
  checkGoal();
  updateGuideState();
  drawMaze();
}

function normalizeRadians(value) {
  let output = value;
  while (output <= -Math.PI) output += Math.PI * 2;
  while (output > Math.PI) output -= Math.PI * 2;
  return output;
}

function getRelativeDirectionLabel() {
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const rightX = Math.cos(facingRad);
  const rightY = Math.sin(facingRad);
  const forwardComponent = toGuideX * forwardX + toGuideY * forwardY;
  const rightComponent = toGuideX * rightX + toGuideY * rightY;
  const relative = Math.atan2(rightComponent, forwardComponent);
  const sector = Math.round(relative / (Math.PI / 4));
  const labels = [
    "Forward",
    "Forward-Right",
    "Right",
    "Back-Right",
    "Back",
    "Back-Left",
    "Left",
    "Forward-Left",
  ];
  return labels[((sector % 8) + 8) % 8];
}

function updateFacingLabel() {
  const cardinalIndex = Math.round(facingDegrees / 90) % 4;
  facingLabel.textContent = `${Math.round(facingDegrees)}° (${CARDINAL_LABELS[cardinalIndex]})`;
}

function updateGuideAudio() {
  if (!audioCtx || !panner || !distanceToneGain || !toneFilter) return;
  const now = audioCtx.currentTime;
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const distance = getDistanceToGuide();
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const forwardComponent = toGuideX * forwardX + toGuideY * forwardY;
  const frontness = Math.max(-1, Math.min(1, forwardComponent / Math.max(distance, 0.001)));

  panner.positionX.setValueAtTime(toGuideX, now);
  panner.positionY.setValueAtTime(0, now);
  panner.positionZ.setValueAtTime(toGuideY, now);

  const distanceFactor = Math.max(0.6, Math.min(1.1, 1.18 - distance * 0.045));
  const nearBoost = Math.max(0, Math.min(0.42, (2.6 - distance) * 0.18));
  const frontScale = (frontness + 1) / 2;
  const directionalGain = 0.62 + frontScale * 0.38;
  distanceToneGain.gain.setTargetAtTime((distanceFactor + nearBoost) * directionalGain, now, 0.04);
  toneFilter.frequency.setTargetAtTime(1800, now, 0.08);
  pulsePeak = 0.32;
}

function updateListener() {
  if (!audioCtx) return;
  const listener = audioCtx.listener;
  const rad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(rad);
  const forwardZ = -Math.cos(rad);
  if (listener.positionX) {
    listener.positionX.setValueAtTime(0, audioCtx.currentTime);
    listener.positionY.setValueAtTime(0, audioCtx.currentTime);
    listener.positionZ.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardX.setValueAtTime(forwardX, audioCtx.currentTime);
    listener.forwardY.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardZ.setValueAtTime(forwardZ, audioCtx.currentTime);
    listener.upX.setValueAtTime(0, audioCtx.currentTime);
    listener.upY.setValueAtTime(1, audioCtx.currentTime);
    listener.upZ.setValueAtTime(0, audioCtx.currentTime);
  } else if (listener.setOrientation) {
    listener.setPosition(0, 0, 0);
    listener.setOrientation(forwardX, 0, forwardZ, 0, 1, 0);
  }
}

function pulseGuide() {
  if (!audioCtx || !distanceToneGain || !toneFilter || guideClipBuffers.length === 0 || mazeCompleted) {
    return;
  }
  const now = audioCtx.currentTime;
  const clipBuffer = guideClipBuffers[guideClipIndex];
  guideClipIndex = (guideClipIndex + 1) % guideClipBuffers.length;
  const source = audioCtx.createBufferSource();
  source.buffer = clipBuffer;
  source.playbackRate.value = 1;
  const pulseGain = audioCtx.createGain();
  pulseGain.gain.setValueAtTime(0.0001, now);
  pulseGain.gain.exponentialRampToValueAtTime(pulsePeak, now + 0.02);
  const clipDuration = Math.min(clipBuffer.duration, Math.max(1.8, pulseIntervalMs / 1000 - 0.15));
  const fadeOutStart = Math.max(now + 0.3, now + clipDuration - 0.16);
  pulseGain.gain.setValueAtTime(pulsePeak, fadeOutStart);
  pulseGain.gain.exponentialRampToValueAtTime(0.0001, now + clipDuration);
  source.connect(pulseGain);
  pulseGain.connect(toneFilter);
  source.start(now);
  source.stop(now + clipDuration);
}

function updatePulseLoop() {
  if (mazeCompleted) {
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
      activePulseIntervalMs = null;
    }
    return;
  }
  if (pulseTimerId && activePulseIntervalMs === pulseIntervalMs) return;
  if (pulseTimerId) clearInterval(pulseTimerId);
  pulseTimerId = setInterval(pulseGuide, pulseIntervalMs);
  activePulseIntervalMs = pulseIntervalMs;
}

function updateGuideState() {
  updateGuideWaypoint();
  const distance = getDistanceToGuide();
  guideDirectionLabel.textContent = getRelativeDirectionLabel();
  distanceLabel.textContent = `${distance.toFixed(1)} cells`;
  if (!mazeCompleted) mazeStatusLabel.textContent = "Follow the guide";
  updateGuideAudio();
  updatePulseLoop();
  maybeWatchOutForObstacle();
}

function checkGoal() {
  if (mazeCompleted) return;
  if (getDistanceToGoal() <= 0.5) {
    mazeCompleted = true;
    mazeStatusLabel.textContent = "Goal reached";
    guideDirectionLabel.textContent = "Done";
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
    }
  }
}

async function loadGuideClipBuffer() {
  if (!audioCtx || guideClipBuffers.length > 0) return;
  for (const url of GUIDE_CLIP_URLS) {
    try {
      const response = await fetch(url);
      if (!response.ok) continue;
      const decoded = await audioCtx.decodeAudioData(await response.arrayBuffer());
      guideClipBuffers.push(decoded);
    } catch {
      // Try next clip.
    }
  }
  for (const [key, url] of Object.entries(JUMP_CLIP_URLS)) {
    try {
      const response = await fetch(url);
      if (!response.ok) continue;
      jumpClipBuffers[key] = await audioCtx.decodeAudioData(await response.arrayBuffer());
    } catch {
      // Keep optional.
    }
  }
}

async function initializeAudio() {
  if (audioCtx) return;
  audioCtx = new AudioContext();
  toneFilter = audioCtx.createBiquadFilter();
  distanceToneGain = audioCtx.createGain();
  panner = audioCtx.createPanner();
  toneFilter.type = "lowpass";
  toneFilter.frequency.value = 2400;
  toneFilter.Q.value = 0.5;
  distanceToneGain.gain.value = 1;
  panner.panningModel = "HRTF";
  panner.distanceModel = "inverse";
  panner.refDistance = 0.9;
  panner.maxDistance = 24;
  panner.rolloffFactor = 1.3;
  panner.coneInnerAngle = 360;
  panner.coneOuterAngle = 0;
  panner.coneOuterGain = 0;
  toneFilter.connect(distanceToneGain);
  distanceToneGain.connect(panner);
  panner.connect(audioCtx.destination);
  await loadGuideClipBuffer();
  if (guideClipBuffers.length === 0) mazeStatusLabel.textContent = "Could not load guide clip";
  updateListener();
  updateGuideState();
  pulseGuide();
}

function regenerateMaze() {
  maze = createMaze(MAZE_WIDTH, MAZE_HEIGHT);
  player = { x: 1.5, y: 1.5 };
  goal = { x: MAZE_WIDTH - 1.5, y: MAZE_HEIGHT - 1.5 };
  guide = { x: 1.5, y: 1.5 };
  mazeCompleted = false;
  jumpObstacles = [];
  jumpActiveUntilMs = 0;
  lastJumpPromptAtMs = 0;
  lastWatchOutPromptAtMs = 0;
  generateJumpObstacles();
  updateJumpLabel();
  updateGuideState();
  drawMaze();
}

function drawMaze() {
  const width = canvas.width;
  const height = canvas.height;
  const cellW = width / MAZE_WIDTH;
  const cellH = height / MAZE_HEIGHT;
  const wallInset = Math.min(cellW, cellH) * WALL_THICKNESS;
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, width, height);
  for (let y = 0; y < MAZE_HEIGHT; y += 1) {
    for (let x = 0; x < MAZE_WIDTH; x += 1) {
      if (maze[y]?.[x] !== 1) continue;
      ctx.fillStyle = "#1f1f1f";
      ctx.fillRect(
        x * cellW + wallInset,
        y * cellH + wallInset,
        cellW - wallInset * 2,
        cellH - wallInset * 2
      );
    }
  }

  const goalX = goal.x * cellW;
  const goalY = goal.y * cellH;
  const guideX = guide.x * cellW;
  const guideY = guide.y * cellH;
  ctx.fillStyle = mazeCompleted ? "#8ae68a" : "#10b981";
  ctx.beginPath();
  ctx.arc(goalX, goalY, Math.min(cellW, cellH) * 0.22, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#f97316";
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.28, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "#f97316";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.48, 0, Math.PI * 2);
  ctx.stroke();

  for (const obstacle of jumpObstacles) {
    if (obstacle.cleared) continue;
    const ox = obstacle.x * cellW;
    const oy = obstacle.y * cellH;
    ctx.fillStyle = "#facc15";
    ctx.fillRect(ox - cellW * 0.24, oy - cellH * 0.11, cellW * 0.48, cellH * 0.22);
    ctx.strokeStyle = "#a16207";
    ctx.lineWidth = 1.5;
    ctx.strokeRect(ox - cellW * 0.24, oy - cellH * 0.11, cellW * 0.48, cellH * 0.22);
  }

  const px = player.x * cellW;
  const py = player.y * cellH;
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(px, py, Math.min(cellW, cellH) * 0.24, 0, Math.PI * 2);
  ctx.fill();

  const rad = (facingDegrees * Math.PI) / 180;
  const arrowLength = Math.min(cellW, cellH) * 0.7;
  ctx.strokeStyle = "#e5e5e5";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(px, py);
  ctx.lineTo(px + Math.sin(rad) * arrowLength, py - Math.cos(rad) * arrowLength);
  ctx.stroke();

  ctx.fillStyle = "#f3f4f6";
  ctx.font = "12px Arial";
  ctx.fillText("Guide Sound", guideX + 8, guideY - 8);
  ctx.fillText("Goal", goalX + 8, goalY + 14);
}

function enableControls() {
  newMazeButton.disabled = false;
  intervalSlider.disabled = false;
  facingSlider.disabled = false;
}

function updateIntervalLabel() {
  intervalValue.textContent = `${(pulseIntervalMs / 1000).toFixed(1)}s`;
}

startButton.addEventListener("click", async () => {
  await initializeAudio();
  if (audioCtx.state === "suspended") await audioCtx.resume();
  enableControls();
  startButton.disabled = true;
  startButton.textContent = "Audio Running";
  regenerateMaze();
});

newMazeButton.addEventListener("click", () => {
  regenerateMaze();
});

intervalSlider.addEventListener("input", (event) => {
  pulseIntervalMs = Math.round(Number(event.target.value) * 1000);
  updateIntervalLabel();
  if (!facingSlider.disabled) updatePulseLoop();
});

facingSlider.addEventListener("input", (event) => {
  facingDegrees = clampAngle(Number(event.target.value));
  updateFacingLabel();
  updateListener();
  updateGuideState();
  drawMaze();
});

window.addEventListener("keydown", (event) => {
  if (facingSlider.disabled) return;
  const key = event.key.toLowerCase();
  if (event.code === "Space") {
    event.preventDefault();
    jumpActiveUntilMs = nowMs() + 700;
    updateJumpLabel();
    playPrompt("jump", true);
    return;
  }
  if (key === "w") {
    event.preventDefault();
    movePlayer(0, -1);
  } else if (key === "s") {
    event.preventDefault();
    movePlayer(0, 1);
  } else if (key === "a") {
    event.preventDefault();
    movePlayer(-1, 0);
  } else if (key === "d") {
    event.preventDefault();
    movePlayer(1, 0);
  } else if (event.key === "ArrowLeft") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees - 15);
    facingSlider.value = String(Math.round(facingDegrees));
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  } else if (event.key === "ArrowRight") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees + 15);
    facingSlider.value = String(Math.round(facingDegrees));
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  }
});

window.addEventListener("beforeunload", () => {
  if (pulseTimerId) clearInterval(pulseTimerId);
  if (audioCtx) audioCtx.close();
});

maze = createMaze(MAZE_WIDTH, MAZE_HEIGHT);
generateJumpObstacles();
updateIntervalLabel();
updateJumpLabel();
updateFacingLabel();
drawMaze();
/*
const startButton = document.getElementById("startButton");
const newMazeButton = document.getElementById("newMazeButton");
const intervalSlider = document.getElementById("intervalSlider");
const intervalValue = document.getElementById("intervalValue");
const facingSlider = document.getElementById("facingSlider");
const facingLabel = document.getElementById("facingLabel");
const guideDirectionLabel = document.getElementById("guideDirectionLabel");
const distanceLabel = document.getElementById("distanceLabel");
const crouchLabel = document.getElementById("crouchLabel");
const mazeStatusLabel = document.getElementById("mazeStatusLabel");
const canvas = document.getElementById("topDownCanvas");
const ctx = canvas.getContext("2d");

const MAZE_WIDTH = 13;
const MAZE_HEIGHT = 13;
const MOVE_STEP = 0.22;
const PLAYER_RADIUS = 0.16;
const WALL_THICKNESS = 0.13;
const MONSTER_COUNT = 3;
const MONSTER_STEP_MS = 120;
const MONSTER_CATCH_RADIUS = 0.58;
const MONSTER_CROUCH_RADIUS = 0.3;
const MONSTER_WARNING_RADIUS = 2.2;

const CARDINAL_LABELS = ["North", "East", "South", "West"];
const GUIDE_CLIP_URLS = [
  "./generated_game_voice_lines/bright_adventurer_01_this_way.wav",
  "./generated_game_voice_lines/bright_adventurer_01_over_here.wav",
  "./generated_game_voice_lines/bright_adventurer_01_come_here.wav",
  "./generated_game_voice_lines/bright_adventurer_04_quickly_lets_go.wav",
];
const WARNING_CLIP_URLS = {
  crouch: "./generated_game_voice_lines/bright_adventurer_03_crouch.wav",
  quiet: "./generated_game_voice_lines/bright_adventurer_03_monster_quiet.wav",
  watchOut: "./generated_game_voice_lines/bright_adventurer_02_watch_out_jump.wav",
};

let audioCtx = null;
let toneFilter = null;
let distanceToneGain = null;
let panner = null;
let guideClipBuffers = [];
let guideClipIndex = 0;
let warningClipBuffers = { crouch: null, quiet: null, watchOut: null };
let pulseTimerId = null;
let activePulseIntervalMs = null;
let monsterTimerId = null;
let pulsePeak = 0.3;
let pulseIntervalMs = 2400;

let facingDegrees = 0;
let maze = [];
let player = { x: 1.5, y: 1.5 };
let goal = { x: MAZE_WIDTH - 1.5, y: MAZE_HEIGHT - 1.5 };
let guide = { x: 1.5, y: 1.5 };
let monsters = [];
let isCrouching = false;
let isCaught = false;
let lastWarningAtMs = 0;
let lastWarningType = "";
let mazeCompleted = false;

function clampAngle(value) {
  const normalized = value % 360;
  return normalized < 0 ? normalized + 360 : normalized;
}

function createMaze(width, height) {
  const grid = Array.from({ length: height }, () => Array(width).fill(1));

  function shuffle(values) {
    const copy = [...values];
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function carve(x, y) {
    grid[y][x] = 0;
    const dirs = shuffle([
      [2, 0],
      [-2, 0],
      [0, 2],
      [0, -2],
    ]);
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx <= 0 || ny <= 0 || nx >= width - 1 || ny >= height - 1) continue;
      if (grid[ny][nx] !== 1) continue;
      grid[y + dy / 2][x + dx / 2] = 0;
      carve(nx, ny);
    }
  }

  carve(1, 1);
  grid[1][1] = 0;
  grid[height - 2][width - 2] = 0;
  return grid;
}

function isWallAt(x, y) {
  const gridX = Math.floor(x);
  const gridY = Math.floor(y);
  if (gridX < 0 || gridY < 0 || gridX >= MAZE_WIDTH || gridY >= MAZE_HEIGHT) return true;
  return maze[gridY][gridX] === 1;
}

function canMoveTo(x, y) {
  return (
    !isWallAt(x - PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y - PLAYER_RADIUS) &&
    !isWallAt(x - PLAYER_RADIUS, y + PLAYER_RADIUS) &&
    !isWallAt(x + PLAYER_RADIUS, y + PLAYER_RADIUS)
  );
}

function shuffleArray(values) {
  const copy = [...values];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function cellCenter(cell) {
  return { x: cell.x + 0.5, y: cell.y + 0.5 };
}

function distance2d(ax, ay, bx, by) {
  const dx = ax - bx;
  const dy = ay - by;
  return Math.sqrt(dx * dx + dy * dy);
}

function spawnMonsters() {
  const candidates = [];
  for (let y = 1; y < MAZE_HEIGHT - 1; y += 1) {
    for (let x = 1; x < MAZE_WIDTH - 1; x += 1) {
      if (maze[y][x] !== 0) continue;
      const startDistance = distance2d(x + 0.5, y + 0.5, 1.5, 1.5);
      const goalDistance = distance2d(x + 0.5, y + 0.5, goal.x, goal.y);
      if (startDistance < 3.2 || goalDistance < 2.2) continue;
      candidates.push({ x, y });
    }
  }

  monsters = [];
  for (const anchor of shuffleArray(candidates)) {
    if (monsters.length >= MONSTER_COUNT) break;
    const horizontalOpen = maze[anchor.y][anchor.x - 1] === 0 && maze[anchor.y][anchor.x + 1] === 0;
    const verticalOpen = maze[anchor.y - 1][anchor.x] === 0 && maze[anchor.y + 1][anchor.x] === 0;
    if (!horizontalOpen && !verticalOpen) continue;

    const horizontal = horizontalOpen && (!verticalOpen || Math.random() > 0.5);
    let start = { x: anchor.x, y: anchor.y };
    let end = { x: anchor.x, y: anchor.y };
    const maxLen = 2 + Math.floor(Math.random() * 2);

    if (horizontal) {
      let left = anchor.x;
      let right = anchor.x;
      for (let i = 0; i < maxLen && maze[anchor.y][left - 1] === 0; i += 1) left -= 1;
      for (let i = 0; i < maxLen && maze[anchor.y][right + 1] === 0; i += 1) right += 1;
      start = { x: left, y: anchor.y };
      end = { x: right, y: anchor.y };
    } else {
      let up = anchor.y;
      let down = anchor.y;
      for (let i = 0; i < maxLen && maze[up - 1][anchor.x] === 0; i += 1) up -= 1;
      for (let i = 0; i < maxLen && maze[down + 1][anchor.x] === 0; i += 1) down += 1;
      start = { x: anchor.x, y: up };
      end = { x: anchor.x, y: down };
    }

    if (start.x === end.x && start.y === end.y) continue;
    monsters.push({
      start,
      end,
      t: Math.random(),
      dir: Math.random() > 0.5 ? 1 : -1,
      speed: 0.55 + Math.random() * 0.45,
      x: anchor.x + 0.5,
      y: anchor.y + 0.5,
    });
  }
}

function movePlayer(localX, localY) {
  if (mazeCompleted || isCaught) return;
  const rad = (facingDegrees * Math.PI) / 180;
  const worldX = localX * Math.cos(rad) - localY * Math.sin(rad);
  const worldY = localX * Math.sin(rad) + localY * Math.cos(rad);
  const stepSize = MOVE_STEP * (isCrouching ? 0.45 : 1);

  const nextX = player.x + worldX * stepSize;
  const nextY = player.y + worldY * stepSize;

  let finalX = player.x;
  let finalY = player.y;
  if (canMoveTo(nextX, player.y)) finalX = nextX;
  if (canMoveTo(finalX, nextY)) finalY = nextY;

  player.x = Math.min(MAZE_WIDTH - 1.01, Math.max(1.01, finalX));
  player.y = Math.min(MAZE_HEIGHT - 1.01, Math.max(1.01, finalY));

  checkMonsterCollision();
  checkGoal();
  updateGuideState();
  drawMaze();
}

function getDistanceToGoal() {
  const dx = goal.x - player.x;
  const dy = goal.y - player.y;
  return Math.sqrt(dx * dx + dy * dy);
}

function getDistanceToGuide() {
  const dx = guide.x - player.x;
  const dy = guide.y - player.y;
  return Math.sqrt(dx * dx + dy * dy);
}

function getPlayerCell() {
  return { x: Math.floor(player.x), y: Math.floor(player.y) };
}

function getGoalCell() {
  return { x: Math.floor(goal.x), y: Math.floor(goal.y) };
}

function getCellKey(x, y) {
  return `${x},${y}`;
}

function computePathBfs(startCell, endCell) {
  const queue = [startCell];
  const visited = new Set([getCellKey(startCell.x, startCell.y)]);
  const parent = new Map();
  const moves = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
  ];

  while (queue.length) {
    const current = queue.shift();
    if (current.x === endCell.x && current.y === endCell.y) break;
    for (const [dx, dy] of moves) {
      const nx = current.x + dx;
      const ny = current.y + dy;
      if (nx < 0 || ny < 0 || nx >= MAZE_WIDTH || ny >= MAZE_HEIGHT) continue;
      if (maze[ny][nx] === 1) continue;
      const key = getCellKey(nx, ny);
      if (visited.has(key)) continue;
      visited.add(key);
      parent.set(key, current);
      queue.push({ x: nx, y: ny });
    }
  }

  const endKey = getCellKey(endCell.x, endCell.y);
  if (!visited.has(endKey)) return [];

  const path = [];
  let current = endCell;
  while (current) {
    path.push(current);
    const key = getCellKey(current.x, current.y);
    current = parent.get(key) || null;
  }
  path.reverse();
  return path;
}

function chooseGuideCellFromPath(path) {
  if (path.length <= 1) return path[0] || getGoalCell();
  if (path.length === 2) return path[1];

  const initialDx = path[1].x - path[0].x;
  const initialDy = path[1].y - path[0].y;
  let index = 1;
  while (index + 1 < path.length) {
    const nextDx = path[index + 1].x - path[index].x;
    const nextDy = path[index + 1].y - path[index].y;
    if (nextDx !== initialDx || nextDy !== initialDy) {
      return path[index];
    }
    index += 1;
  }
  return path[path.length - 1];
}

function updateGuideWaypoint() {
  const path = computePathBfs(getPlayerCell(), getGoalCell());
  const waypointCell = chooseGuideCellFromPath(path);
  guide = { x: waypointCell.x + 0.5, y: waypointCell.y + 0.5 };
}

function distancePointToSegment(px, py, ax, ay, bx, by) {
  const abx = bx - ax;
  const aby = by - ay;
  const apx = px - ax;
  const apy = py - ay;
  const lenSq = abx * abx + aby * aby;
  if (lenSq === 0) return distance2d(px, py, ax, ay);
  const t = Math.max(0, Math.min(1, (apx * abx + apy * aby) / lenSq));
  const sx = ax + abx * t;
  const sy = ay + aby * t;
  return distance2d(px, py, sx, sy);
}

function isMonsterBlockingGuide(monster) {
  const toGuide = distancePointToSegment(monster.x, monster.y, player.x, player.y, guide.x, guide.y);
  const distFromPlayer = distance2d(monster.x, monster.y, player.x, player.y);
  return toGuide < 0.48 && distFromPlayer < 3.6;
}

function updateMonsters(deltaSec) {
  if (mazeCompleted || isCaught || monsters.length === 0) return;
  for (const monster of monsters) {
    const start = cellCenter(monster.start);
    const end = cellCenter(monster.end);
    const segmentLength = Math.max(0.001, distance2d(start.x, start.y, end.x, end.y));
    monster.t += (monster.speed * deltaSec * monster.dir) / segmentLength;
    if (monster.t > 1) {
      monster.t = 2 - monster.t;
      monster.dir *= -1;
    } else if (monster.t < 0) {
      monster.t = -monster.t;
      monster.dir *= -1;
    }
    monster.x = start.x + (end.x - start.x) * monster.t;
    monster.y = start.y + (end.y - start.y) * monster.t;
  }

  checkMonsterCollision();
  updateGuideState();
  drawMaze();
}

function playWarning(type, force = false) {
  if (!audioCtx || audioCtx.state !== "running") return;
  const buffer = warningClipBuffers[type];
  if (!buffer) return;
  const nowMs = Date.now();
  if (!force && nowMs - lastWarningAtMs < 3200) return;
  lastWarningAtMs = nowMs;
  lastWarningType = type;

  const source = audioCtx.createBufferSource();
  source.buffer = buffer;
  const gain = audioCtx.createGain();
  gain.gain.value = 0.9;
  source.connect(gain);
  gain.connect(audioCtx.destination);
  source.start();
}

function checkMonsterCollision() {
  if (isCaught || mazeCompleted) return;
  let nearestDistance = Infinity;
  let blockingMonsterExists = false;
  for (const monster of monsters) {
    const d = distance2d(player.x, player.y, monster.x, monster.y);
    nearestDistance = Math.min(nearestDistance, d);
    if (isMonsterBlockingGuide(monster)) blockingMonsterExists = true;
    const catchRadius = isCrouching ? MONSTER_CROUCH_RADIUS : MONSTER_CATCH_RADIUS;
    if (d <= catchRadius) {
      isCaught = true;
      mazeStatusLabel.textContent = "Caught by monster - New Maze to retry";
      guideDirectionLabel.textContent = "Danger";
      playWarning("watchOut", true);
      if (pulseTimerId) {
        clearInterval(pulseTimerId);
        pulseTimerId = null;
      }
      if (monsterTimerId) {
        clearInterval(monsterTimerId);
        monsterTimerId = null;
      }
      return;
    }
  }

  if (nearestDistance < MONSTER_WARNING_RADIUS || blockingMonsterExists) {
    if (isCrouching) {
      playWarning("quiet");
    } else if (blockingMonsterExists) {
      playWarning("crouch");
      mazeStatusLabel.textContent = "Monster ahead - crouch and wait";
    } else {
      playWarning("watchOut");
    }
  }
}

function normalizeRadians(value) {
  let output = value;
  while (output <= -Math.PI) output += Math.PI * 2;
  while (output > Math.PI) output -= Math.PI * 2;
  return output;
}

function getRelativeDirectionLabel() {
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const rightX = Math.cos(facingRad);
  const rightY = Math.sin(facingRad);

  const forwardComponent = toGuideX * forwardX + toGuideY * forwardY;
  const rightComponent = toGuideX * rightX + toGuideY * rightY;
  const relative = Math.atan2(rightComponent, forwardComponent);
  const sector = Math.round(relative / (Math.PI / 4));

  const labels = [
    "Forward",
    "Forward-Right",
    "Right",
    "Back-Right",
    "Back",
    "Back-Left",
    "Left",
    "Forward-Left",
  ];
  const wrapped = ((sector % 8) + 8) % 8;
  return labels[wrapped];
}

function updateFacingLabel() {
  const cardinalIndex = Math.round(facingDegrees / 90) % 4;
  facingLabel.textContent = `${Math.round(facingDegrees)}° (${CARDINAL_LABELS[cardinalIndex]})`;
}

function updateGuideAudio() {
  if (!audioCtx || !panner || !distanceToneGain || !toneFilter || isCaught) return;
  const now = audioCtx.currentTime;
  const toGuideX = guide.x - player.x;
  const toGuideY = guide.y - player.y;
  const distance = getDistanceToGuide();
  const facingRad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(facingRad);
  const forwardY = -Math.cos(facingRad);
  const forwardComponent = toGuideX * forwardX + toGuideY * forwardY;
  const safeDistance = Math.max(0.001, distance);
  const frontness = Math.max(-1, Math.min(1, forwardComponent / safeDistance));

  // Feed world-space source position; listener orientation handles left/right/front/back.
  panner.positionX.setValueAtTime(toGuideX, now);
  panner.positionY.setValueAtTime(0, now);
  panner.positionZ.setValueAtTime(toGuideY, now);

  // Keep voice natural: only back attenuation + mild distance attenuation.
  const distanceFactor = Math.max(0.6, Math.min(1.1, 1.18 - distance * 0.045));
  const nearBoost = Math.max(0, Math.min(0.42, (2.6 - distance) * 0.18));
  const frontScale = (frontness + 1) / 2;
  const directionalGain = 0.62 + frontScale * 0.38;

  distanceToneGain.gain.setTargetAtTime(
    (distanceFactor + nearBoost) * directionalGain,
    now,
    0.04
  );
  toneFilter.frequency.setTargetAtTime(1800, now, 0.08);
  pulsePeak = 0.32;
}

function updateListener() {
  if (!audioCtx) return;
  const listener = audioCtx.listener;
  const rad = (facingDegrees * Math.PI) / 180;
  const forwardX = Math.sin(rad);
  const forwardZ = -Math.cos(rad);

  if (listener.positionX) {
    listener.positionX.setValueAtTime(0, audioCtx.currentTime);
    listener.positionY.setValueAtTime(0, audioCtx.currentTime);
    listener.positionZ.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardX.setValueAtTime(forwardX, audioCtx.currentTime);
    listener.forwardY.setValueAtTime(0, audioCtx.currentTime);
    listener.forwardZ.setValueAtTime(forwardZ, audioCtx.currentTime);
    listener.upX.setValueAtTime(0, audioCtx.currentTime);
    listener.upY.setValueAtTime(1, audioCtx.currentTime);
    listener.upZ.setValueAtTime(0, audioCtx.currentTime);
  } else if (listener.setOrientation) {
    listener.setPosition(0, 0, 0);
    listener.setOrientation(forwardX, 0, forwardZ, 0, 1, 0);
  }
}

function pulseGuide() {
  if (
    !audioCtx ||
    !distanceToneGain ||
    !toneFilter ||
    guideClipBuffers.length === 0 ||
    mazeCompleted
  ) {
    return;
  }
  const now = audioCtx.currentTime;
  const clipBuffer = guideClipBuffers[guideClipIndex];
  guideClipIndex = (guideClipIndex + 1) % guideClipBuffers.length;

  const source = audioCtx.createBufferSource();
  source.buffer = clipBuffer;
  source.playbackRate.value = 1;

  const pulseGain = audioCtx.createGain();
  pulseGain.gain.setValueAtTime(0.0001, now);
  pulseGain.gain.exponentialRampToValueAtTime(pulsePeak, now + 0.02);

  const clipDuration = Math.min(
    clipBuffer.duration,
    Math.max(1.8, pulseIntervalMs / 1000 - 0.15)
  );
  const fadeOutStart = Math.max(now + 0.3, now + clipDuration - 0.16);
  pulseGain.gain.setValueAtTime(pulsePeak, fadeOutStart);
  pulseGain.gain.exponentialRampToValueAtTime(0.0001, now + clipDuration);

  source.connect(pulseGain);
  pulseGain.connect(toneFilter);
  source.start(now);
  source.stop(now + clipDuration);
}

function updatePulseLoop() {
  if (mazeCompleted || isCaught) {
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
      activePulseIntervalMs = null;
    }
    return;
  }

  if (pulseTimerId && activePulseIntervalMs === pulseIntervalMs) return;
  if (pulseTimerId) clearInterval(pulseTimerId);
  pulseTimerId = setInterval(pulseGuide, pulseIntervalMs);
  activePulseIntervalMs = pulseIntervalMs;
}

function updateGuideState() {
  updateGuideWaypoint();
  const distance = getDistanceToGuide();
  const relativeLabel = getRelativeDirectionLabel();
  guideDirectionLabel.textContent = relativeLabel;
  distanceLabel.textContent = `${distance.toFixed(1)} cells`;
  if (!isCaught) {
    mazeStatusLabel.textContent = mazeCompleted ? "Goal reached" : "Follow the guide";
  }
  updateGuideAudio();
  updatePulseLoop();
}

function checkGoal() {
  if (mazeCompleted || isCaught) return;
  const distance = getDistanceToGoal();
  if (distance <= 0.5) {
    mazeCompleted = true;
    mazeStatusLabel.textContent = "Goal reached";
    guideDirectionLabel.textContent = "Done";
    if (pulseTimerId) {
      clearInterval(pulseTimerId);
      pulseTimerId = null;
    }
  }
}

async function loadGuideClipBuffer() {
  if (!audioCtx || guideClipBuffers.length > 0) return;
  for (const url of GUIDE_CLIP_URLS) {
    try {
      const response = await fetch(url);
      if (!response.ok) continue;
      const arrayBuffer = await response.arrayBuffer();
      const decoded = await audioCtx.decodeAudioData(arrayBuffer);
      guideClipBuffers.push(decoded);
    } catch {
      // Try next candidate clip.
    }
  }

  for (const [key, url] of Object.entries(WARNING_CLIP_URLS)) {
    try {
      const response = await fetch(url);
      if (!response.ok) continue;
      const arrayBuffer = await response.arrayBuffer();
      warningClipBuffers[key] = await audioCtx.decodeAudioData(arrayBuffer);
    } catch {
      // Keep warning optional if a clip fails.
    }
  }
}

async function initializeAudio() {
  if (audioCtx) return;
  audioCtx = new AudioContext();
  toneFilter = audioCtx.createBiquadFilter();
  distanceToneGain = audioCtx.createGain();
  panner = audioCtx.createPanner();
  toneFilter.type = "lowpass";
  toneFilter.frequency.value = 2400;
  toneFilter.Q.value = 0.5;

  distanceToneGain.gain.value = 1;

  panner.panningModel = "HRTF";
  panner.distanceModel = "inverse";
  panner.refDistance = 0.9;
  panner.maxDistance = 24;
  panner.rolloffFactor = 1.3;
  panner.coneInnerAngle = 360;
  panner.coneOuterAngle = 0;
  panner.coneOuterGain = 0;

  toneFilter.connect(distanceToneGain);
  distanceToneGain.connect(panner);
  panner.connect(audioCtx.destination);

  await loadGuideClipBuffer();
  if (guideClipBuffers.length === 0) {
    mazeStatusLabel.textContent = "Could not load guide clip";
  }

  updateListener();
  updateGuideState();
  pulseGuide();
}

function regenerateMaze() {
  maze = createMaze(MAZE_WIDTH, MAZE_HEIGHT);
  player = { x: 1.5, y: 1.5 };
  goal = { x: MAZE_WIDTH - 1.5, y: MAZE_HEIGHT - 1.5 };
  guide = { x: 1.5, y: 1.5 };
  monsters = [];
  isCaught = false;
  lastWarningAtMs = 0;
  lastWarningType = "";
  isCrouching = false;
  mazeCompleted = false;
  spawnMonsters();
  updateCrouchLabel();
  updateGuideState();
  if (audioCtx && audioCtx.state === "running") {
    startMonsterLoop();
  }
  drawMaze();
}

function drawMaze() {
  const width = canvas.width;
  const height = canvas.height;
  const cellW = width / MAZE_WIDTH;
  const cellH = height / MAZE_HEIGHT;
  const wallInset = Math.min(cellW, cellH) * WALL_THICKNESS;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, width, height);

  for (let y = 0; y < MAZE_HEIGHT; y += 1) {
    for (let x = 0; x < MAZE_WIDTH; x += 1) {
      if (maze[y]?.[x] !== 1) continue;
      const drawX = x * cellW + wallInset;
      const drawY = y * cellH + wallInset;
      ctx.fillStyle = "#1f1f1f";
      ctx.fillRect(drawX, drawY, cellW - wallInset * 2, cellH - wallInset * 2);
    }
  }

  const goalX = goal.x * cellW;
  const goalY = goal.y * cellH;
  const guideX = guide.x * cellW;
  const guideY = guide.y * cellH;

  // Final maze destination.
  ctx.fillStyle = mazeCompleted ? "#8ae68a" : "#10b981";
  ctx.beginPath();
  ctx.arc(goalX, goalY, Math.min(cellW, cellH) * 0.22, 0, Math.PI * 2);
  ctx.fill();

  // Moving guide/fairy: this is where the sound is produced.
  ctx.fillStyle = "#f97316";
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.28, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "#f97316";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(guideX, guideY, Math.min(cellW, cellH) * 0.48, 0, Math.PI * 2);
  ctx.stroke();

  const px = player.x * cellW;
  const py = player.y * cellH;
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(px, py, Math.min(cellW, cellH) * 0.24, 0, Math.PI * 2);
  ctx.fill();

  const arrowLength = Math.min(cellW, cellH) * 0.7;
  const rad = (facingDegrees * Math.PI) / 180;
  const arrowX = px + Math.sin(rad) * arrowLength;
  const arrowY = py - Math.cos(rad) * arrowLength;
  ctx.strokeStyle = "#e5e5e5";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(px, py);
  ctx.lineTo(arrowX, arrowY);
  ctx.stroke();

  ctx.strokeStyle = "#374151";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(px, py);
  ctx.lineTo(guideX, guideY);
  ctx.stroke();

  ctx.fillStyle = "#f3f4f6";
  ctx.font = "12px Arial";
  ctx.fillText("Guide Sound", guideX + 8, guideY - 8);
  ctx.fillText("Goal", goalX + 8, goalY + 14);

  for (const monster of monsters) {
    const mx = monster.x * cellW;
    const my = monster.y * cellH;
    ctx.fillStyle = "#ef4444";
    ctx.beginPath();
    ctx.arc(mx, my, Math.min(cellW, cellH) * 0.24, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#7f1d1d";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(mx, my, Math.min(cellW, cellH) * 0.36, 0, Math.PI * 2);
    ctx.stroke();
  }
}

function enableControls() {
  newMazeButton.disabled = false;
  intervalSlider.disabled = false;
  facingSlider.disabled = false;
}

function updateIntervalLabel() {
  intervalValue.textContent = `${(pulseIntervalMs / 1000).toFixed(1)}s`;
}

function updateCrouchLabel() {
  crouchLabel.textContent = isCrouching ? "On" : "Off";
}

function startMonsterLoop() {
  if (monsterTimerId) clearInterval(monsterTimerId);
  monsterTimerId = setInterval(() => {
    updateMonsters(MONSTER_STEP_MS / 1000);
  }, MONSTER_STEP_MS);
}

startButton.addEventListener("click", async () => {
  await initializeAudio();
  if (audioCtx.state === "suspended") {
    await audioCtx.resume();
  }
  enableControls();
  startButton.disabled = true;
  startButton.textContent = "Audio Running";
  regenerateMaze();
});

newMazeButton.addEventListener("click", () => {
  regenerateMaze();
});

intervalSlider.addEventListener("input", (event) => {
  pulseIntervalMs = Math.round(Number(event.target.value) * 1000);
  updateIntervalLabel();
  if (!facingSlider.disabled) {
    updatePulseLoop();
  }
});

facingSlider.addEventListener("input", (event) => {
  facingDegrees = clampAngle(Number(event.target.value));
  updateFacingLabel();
  updateListener();
  updateGuideState();
  drawMaze();
});

window.addEventListener("keydown", (event) => {
  if (facingSlider.disabled) return;
  const key = event.key.toLowerCase();
  if (event.key === "Shift") {
    if (!isCrouching) {
      isCrouching = true;
      updateCrouchLabel();
      if (!mazeCompleted && !isCaught) playWarning("quiet");
    }
    return;
  }
  if (key === "c") {
    isCrouching = !isCrouching;
    updateCrouchLabel();
    if (isCrouching && !mazeCompleted && !isCaught) playWarning("crouch");
    return;
  }
  if (key === "w") {
    event.preventDefault();
    movePlayer(0, -1);
  } else if (key === "s") {
    event.preventDefault();
    movePlayer(0, 1);
  } else if (key === "a") {
    event.preventDefault();
    movePlayer(-1, 0);
  } else if (key === "d") {
    event.preventDefault();
    movePlayer(1, 0);
  } else if (event.key === "ArrowLeft") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees - 15);
    facingSlider.value = String(Math.round(facingDegrees));
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  } else if (event.key === "ArrowRight") {
    event.preventDefault();
    facingDegrees = clampAngle(facingDegrees + 15);
    facingSlider.value = String(Math.round(facingDegrees));
    updateFacingLabel();
    updateListener();
    updateGuideState();
    drawMaze();
  }
});

window.addEventListener("keyup", (event) => {
  if (event.key !== "Shift") return;
  isCrouching = false;
  updateCrouchLabel();
});

window.addEventListener("beforeunload", () => {
  if (pulseTimerId) clearInterval(pulseTimerId);
  if (monsterTimerId) clearInterval(monsterTimerId);
  if (audioCtx) audioCtx.close();
});

maze = createMaze(MAZE_WIDTH, MAZE_HEIGHT);
spawnMonsters();
updateIntervalLabel();
updateCrouchLabel();
updateFacingLabel();
drawMaze();
*/
