# app/avatar.py
from pathlib import Path
import base64, textwrap, os

_HTML = """<!doctype html><html lang="en"><meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>3D Avatar</title>
<body style="margin:0;background:__BACKGROUND__">
<div id="root" style="position:relative;width:100%;height:__HEIGHT__px;background:__BACKGROUND__"></div>

<button id="resetBtn" style="
  position:absolute; right:12px; top:12px; z-index:10;
  padding:8px 10px; border:0; border-radius:10px;
  background:#ffffff1a; color:#e2e8f0; backdrop-filter: blur(6px);
  font:600 12px system-ui; cursor:pointer;
">↺ Reset View</button>

<!-- Import map (must be before the module script) -->
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
  }
}
</script>

<script type="module">
import * as THREE from 'three';
import { GLTFLoader }      from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader }     from 'three/addons/loaders/DRACOLoader.js';
import { OrbitControls }   from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const root = document.getElementById('root');

// Scene / Camera
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, root.clientWidth / root.clientHeight, 0.1, 5000);
camera.position.set(0, 1.4, 6);

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(root.clientWidth, root.clientHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = __EXPOSURE__;
root.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = __AUTOROTATE__;
controls.autoRotateSpeed = 0.75;

// Environment (lighting only; visual bg via CSS)
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
scene.background = null;

// Optional grid
if (__SHOW_GRID__) {
  const grid = new THREE.GridHelper(10, 20);
  grid.position.y = 0;
  scene.add(grid);
}

// Touch-up PBR
function tunePBR(rootNode){
  rootNode.traverse(n => {
    if (n.isMesh){
      n.castShadow = n.receiveShadow = true;
      const m = n.material;
      if (m && m.isMeshStandardMaterial){
        m.envMapIntensity = __ENV_INTENSITY__;
        m.needsUpdate = true;
      }
      // Be safe about texture color space when present
      const maps = ['map','emissiveMap','metalnessMap','roughnessMap','normalMap'];
      maps.forEach(k => {
        if (m[k] && m[k].isTexture && m[k].colorSpace === undefined) {
          m[k].colorSpace = (k === 'map' || k === 'emissiveMap') ? THREE.SRGBColorSpace : THREE.LinearSRGBColorSpace;
          m[k].needsUpdate = true;
        }
      });
    }
  });
}

// --- framing helpers ---
function findFirst(root, names){
  for (const n of names){
    const o = root.getObjectByName(n);
    if (o) return o;
  }
  return null;
}
function findHead(root){
  return findFirst(root, [
    "Head","head","Head_","HeadTop_End",
    "mixamorigHead","mixamorig:Head","J_Head","Head_joint"
  ]);
}

/** Center, normalize to ~1.65m, ground to y=0, and fit head→chest. */
function frameBust(object, {camera, controls, renderer}){
  // 1) center on origin
  const box1 = new THREE.Box3().setFromObject(object);
  const size1 = box1.getSize(new THREE.Vector3());
  const center1 = box1.getCenter(new THREE.Vector3());
  object.position.sub(center1);

  // 2) normalize scale
  const targetHeight = 1.65; // meters
  if (size1.y > 1e-5) object.scale.multiplyScalar(targetHeight / size1.y);

  // 3) ground to y=0
  const box2 = new THREE.Box3().setFromObject(object);
  object.position.y -= box2.min.y;

  // 4) recompute size now that it's normalized/grounded
  const box3  = new THREE.Box3().setFromObject(object);
  const size3 = box3.getSize(new THREE.Vector3());

  // 5) pick bust region
  const head = findHead(object);
  const headWorld = new THREE.Vector3();
  const eyeY = head ? head.getWorldPosition(headWorld).y : size3.y * 0.90;
  const chestY  = size3.y * 0.55;
  const regionH = Math.max(0.25, eyeY - chestY);

  // 6) distance to fit region vertically & shoulder width horizontally
  const fov = camera.fov * Math.PI / 180;
  const aspect = renderer.domElement.clientWidth / renderer.domElement.clientHeight;
  const fitByH = regionH / (2 * Math.tan(fov / 2));
  const shoulderW = Math.max(0.28, size3.x * 0.60);
  const fitByW = (shoulderW / aspect) / (2 * Math.tan(fov / 2));
  const dist = Math.max(fitByH, fitByW) * 1.18; // slight padding

  // 7) slight horizontal offset; lower and zoom a bit, plus tilt
  // Keep zoom + offset but raise camera slightly and tilt down
  const zoomFactor = 0.60;
  camera.position.set(
    0.22 * size3.x,
    eyeY * 1.2,              // was 0.85 → raise camera
    dist * zoomFactor
);

  // Lower target a bit so camera points slightly down
  controls.target.set(0, eyeY * 0.80, 0);

  controls.update();
}

// ----- Single GLB (mesh + animation) -----
let mixer = null;
let avatar = null;
const clock = new THREE.Clock();

const b64 = "__GLB_B64__";
const bin = atob(b64);
const bytes = new Uint8Array(bin.length);
for (let i=0;i<bin.length;i++) bytes[i] = bin.charCodeAt(i);

const loader = new GLTFLoader();
const draco  = new DRACOLoader();
draco.setDecoderPath("https://unpkg.com/three@0.160.0/examples/jsm/libs/draco/");
loader.setDRACOLoader(draco);

// Reset button (now that controls & frameBust exist)
document.getElementById('resetBtn')?.addEventListener('click', () => {
  if (avatar) frameBust(avatar, { camera, controls, renderer });
  else controls.reset?.();
});

loader.parse(bytes.buffer, "", (gltf) => {
  avatar = gltf.scene;
  tunePBR(avatar);
  scene.add(avatar);

  // Play first clip if present
  if (gltf.animations && gltf.animations.length){
    mixer = new THREE.AnimationMixer(avatar);
    const action = mixer.clipAction(gltf.animations[0]);
    action.reset().setLoop(THREE.LoopRepeat, Infinity).fadeIn(0.25).play();
  } else {
    console.warn("GLB has no animations.");
  }

  // Initial fit + one more frame later (after skeleton settles)
  frameBust(avatar, { camera, controls, renderer });
  requestAnimationFrame(() => frameBust(avatar, { camera, controls, renderer }));
}, (err) => {
  console.error("Failed to parse GLB:", err);
});

// Animate
(function animate(){
  requestAnimationFrame(animate);
  if (mixer) mixer.update(clock.getDelta());
  controls.update();
  renderer.render(scene, camera);
})();

// Resize (re-fit to keep bust framing consistent)
addEventListener('resize', () => {
  const w = root.clientWidth, h = root.clientHeight;
  camera.aspect = w/h; camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  if (avatar) frameBust(avatar, { camera, controls, renderer });
});
</script>
</body></html>
"""

def avatar_html(
    glb_path: str,                      # e.g. "assets/animations/luna_idle.glb"
    *,
    height_px: int = 640,
    exposure: float = 1.15,
    env_intensity: float = 1.35,
    autorotate: bool = False,
    show_grid: bool = False,
    background: str = "radial-gradient(60% 60% at 50% 35%, #151a22 0%, #0a0b10 60%, #07080b 100%)",
) -> str:
    """Render a single GLB (mesh + embedded animation)."""
    root = Path(__file__).resolve().parent.parent
    abs_path = (root / glb_path).resolve()
    if not abs_path.exists():
        raise FileNotFoundError(f"GLB not found: {abs_path}")

    b64 = base64.b64encode(abs_path.read_bytes()).decode("ascii")
    html = (
        _HTML
        .replace("__GLB_B64__", b64)
        .replace("__HEIGHT__", str(height_px))
        .replace("__EXPOSURE__", str(float(exposure)))
        .replace("__ENV_INTENSITY__", str(float(env_intensity)))
        .replace("__AUTOROTATE__", "true" if autorotate else "false")
        .replace("__SHOW_GRID__", "true" if show_grid else "false")
        .replace("__BACKGROUND__", background)
    )
    return textwrap.dedent(html)

def export_viewer(glb_path: str, out_html: str = "avatar_embed.html", **kwargs) -> str:
    html = avatar_html(glb_path, **kwargs)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.abspath(out_html)
