/**
 * Scroll-driven visual: waterfall → clouds → AWG suction → bottles
 * No text chapters — animation tells the story.
 */
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

function initWaterCycle() {
    const canvas = document.getElementById('waterCanvas');
    const storySection = document.querySelector('.water-story');
    const heroPanel = document.querySelector('.hero-panel');
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (!canvas || !storySection || typeof gsap === 'undefined') return;

    gsap.registerPlugin(ScrollTrigger);

    const isMobile = innerWidth < 768;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let progress = 0;
    let elapsed = 0;

    const clamp = gsap.utils.clamp;
    const lerp = THREE.MathUtils.lerp;

    /* ── Renderer ── */
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: !isMobile, alpha: false });
    renderer.setPixelRatio(Math.min(devicePixelRatio, isMobile ? 1.5 : 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a1628);
    scene.fog = new THREE.FogExp2(0x0a1628, 0.022);

    const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 80);
    camera.position.set(0, 0.2, 5.2);

    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

    scene.add(new THREE.HemisphereLight(0x88bbff, 0x0a1520, 0.55));
    const sun = new THREE.DirectionalLight(0xffffff, 1.1);
    sun.position.set(4, 8, 5);
    scene.add(sun);

    /* ── Sky dome ── */
    const skyGeo = new THREE.SphereGeometry(30, 32, 16);
    const skyMat = new THREE.ShaderMaterial({
        side: THREE.BackSide,
        uniforms: {
            top: { value: new THREE.Color(0x1a3050) },
            bottom: { value: new THREE.Color(0x060d18) }
        },
        vertexShader: `
            varying vec3 vPos;
            void main() {
                vPos = position;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
            uniform vec3 top;
            uniform vec3 bottom;
            varying vec3 vPos;
            void main() {
                float h = normalize(vPos).y * 0.5 + 0.5;
                gl_FragColor = vec4(mix(bottom, top, h), 1.0);
            }
        `
    });
    scene.add(new THREE.Mesh(skyGeo, skyMat));

    /* ── Cliff / waterfall source ── */
    const cliff = new THREE.Mesh(
        new THREE.BoxGeometry(5, 1.2, 0.8),
        new THREE.MeshStandardMaterial({ color: 0x2a3540, roughness: 0.85, metalness: 0.05 })
    );
    cliff.position.set(0, 2.8, -0.5);
    scene.add(cliff);

    /* ── WATERFALL streams (tubes) ── */
    const streamCount = isMobile ? 5 : 9;
    const streams = [];
    const waterMat = new THREE.MeshPhysicalMaterial({
        color: 0xc5ecff,
        metalness: 0.05,
        roughness: 0.02,
        transmission: 0.55,
        thickness: 0.8,
        ior: 1.33,
        transparent: true,
        opacity: 0.95,
        emissive: 0x226688,
        emissiveIntensity: 0.15
    });

    for (let i = 0; i < streamCount; i++) {
        const x = (i / (streamCount - 1) - 0.5) * 2.2;
        const curve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(x, 2.2, 0),
            new THREE.Vector3(x + (Math.random() - 0.5) * 0.15, 1.2, 0.1),
            new THREE.Vector3(x + (Math.random() - 0.5) * 0.2, 0.2, 0.15),
            new THREE.Vector3(x * 0.3, -0.6, 0.2)
        ]);
        const mesh = new THREE.Mesh(
            new THREE.TubeGeometry(curve, 48, 0.1 + Math.random() * 0.06, 10, false),
            waterMat.clone()
        );
        scene.add(mesh);
        streams.push({ mesh, curve, x });
    }

    /* ── Falling droplets (instanced) ── */
    const N = isMobile ? 600 : 1400;
    const dropGeo = new THREE.SphereGeometry(0.028, 6, 6);
    const dropMat = new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        metalness: 0,
        roughness: 0,
        transmission: 0.92,
        thickness: 0.15,
        transparent: true
    });
    const drops = new THREE.InstancedMesh(dropGeo, dropMat, N);
    scene.add(drops);

    const dropState = Array.from({ length: N }, (_, i) => ({
        x: (Math.random() - 0.5) * 2.4,
        y: 4 + Math.random() * 2,
        z: (Math.random() - 0.5) * 0.5,
        vy: 0.025 + Math.random() * 0.035,
        phase: Math.random() * 6.28,
        stream: i % streamCount,
        size: 0.5 + Math.random() * 0.6
    }));

    const dummy = new THREE.Object3D();

    /* ── Pool / mist at waterfall base ── */
    const pool = new THREE.Mesh(
        new THREE.CircleGeometry(1.8, 48),
        new THREE.MeshStandardMaterial({
            color: 0x1a4a60,
            metalness: 0.7,
            roughness: 0.15,
            transparent: true,
            opacity: 0.7
        })
    );
    pool.rotation.x = -Math.PI / 2;
    pool.position.set(0, -0.65, 0.15);
    scene.add(pool);

    /* ── Clouds (sprites that GROW as water collects) ── */
    const cloudGroup = new THREE.Group();
    cloudGroup.position.set(0, -0.2, 0);
    scene.add(cloudGroup);

    function makeCloudTex() {
        const c = document.createElement('canvas');
        c.width = c.height = 512;
        const ctx = c.getContext('2d');
        for (let i = 0; i < 6; i++) {
            const g = ctx.createRadialGradient(
                256 + (Math.random() - 0.5) * 80,
                256 + (Math.random() - 0.5) * 60,
                0, 256, 256, 120 + Math.random() * 80
            );
            g.addColorStop(0, 'rgba(255,255,255,0.9)');
            g.addColorStop(0.5, 'rgba(230,245,255,0.4)');
            g.addColorStop(1, 'rgba(255,255,255,0)');
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, 512, 512);
        }
        const t = new THREE.CanvasTexture(c);
        t.colorSpace = THREE.SRGBColorSpace;
        return t;
    }

    const cloudTex = makeCloudTex();
    const cloudCount = isMobile ? 10 : 18;
    const cloudSprites = [];
    for (let i = 0; i < cloudCount; i++) {
        const mat = new THREE.SpriteMaterial({
            map: cloudTex,
            transparent: true,
            depthWrite: false,
            opacity: 0
        });
        const spr = new THREE.Sprite(mat);
        const bx = (Math.random() - 0.5) * 2.5;
        const by = (Math.random() - 0.5) * 0.6;
        spr.position.set(bx, by, (Math.random() - 0.5) * 0.4);
        spr.userData = { bx, by, seed: Math.random() * 10 };
        cloudGroup.add(spr);
        cloudSprites.push(spr);
    }

    /* ── AWG machine ── */
    const machine = new THREE.Group();
    machine.position.set(0, 0.1, 0.5);
    scene.add(machine);

    const steel = new THREE.MeshStandardMaterial({ color: 0x7a828a, metalness: 0.9, roughness: 0.25 });
    const dark = new THREE.MeshStandardMaterial({ color: 0x2e343c, metalness: 0.85, roughness: 0.35 });

    const body = new THREE.Mesh(new THREE.BoxGeometry(2, 1.1, 0.85), steel);
    machine.add(body);
    const intake = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.42, 0.25, 32), dark);
    intake.position.y = 0.68;
    machine.add(intake);

    const fan = new THREE.Group();
    fan.position.y = 0.72;
    for (let b = 0; b < 8; b++) {
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.55, 0.1), dark);
        blade.rotation.y = (b / 8) * Math.PI * 2;
        fan.add(blade);
    }
    machine.add(fan);

    const outPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.7, 16), steel);
    outPipe.rotation.z = Math.PI / 2;
    outPipe.position.set(1.15, -0.1, 0);
    machine.add(outPipe);

    /* Suction spiral particles */
    const spiralN = isMobile ? 120 : 280;
    const spiralGeo = new THREE.BufferGeometry();
    const spiralPos = new Float32Array(spiralN * 3);
    spiralGeo.setAttribute('position', new THREE.BufferAttribute(spiralPos, 3));
    const spiralMat = new THREE.PointsMaterial({
        color: 0xd8eeff,
        size: isMobile ? 0.04 : 0.055,
        transparent: true,
        opacity: 0,
        depthWrite: false,
        blending: THREE.AdditiveBlending
    });
    const spiral = new THREE.Points(spiralGeo, spiralMat);
    machine.add(spiral);

    const spiralState = Array.from({ length: spiralN }, () => ({
        t: Math.random(),
        angle: Math.random() * Math.PI * 2,
        speed: 0.006 + Math.random() * 0.008
    }));

    /* ── Bottles ── */
    const bottleLine = new THREE.Group();
    bottleLine.position.set(0, -1.05, 0.8);
    scene.add(bottleLine);

    const glassMat = new THREE.MeshPhysicalMaterial({
        color: 0xffffff, metalness: 0, roughness: 0.03,
        transmission: 0.96, thickness: 0.4, ior: 1.5, transparent: true
    });
    const liquidMat = new THREE.MeshPhysicalMaterial({
        color: 0x3aadcc, metalness: 0, roughness: 0.1, transparent: true, opacity: 0.9
    });

    function bottleShape() {
        return [
            new THREE.Vector2(0, 0), new THREE.Vector2(0.12, 0.04),
            new THREE.Vector2(0.11, 0.2), new THREE.Vector2(0.15, 0.5),
            new THREE.Vector2(0.16, 0.88), new THREE.Vector2(0.14, 0.98), new THREE.Vector2(0, 0.98)
        ];
    }

    const bottleN = isMobile ? 3 : 5;
    const bottles = [];
    const spacing = 0.44;
    for (let i = 0; i < bottleN; i++) {
        const g = new THREE.Group();
        g.position.x = (i - (bottleN - 1) / 2) * spacing;
        const glass = new THREE.Mesh(new THREE.LatheGeometry(bottleShape(), 40), glassMat);
        const liquid = new THREE.Mesh(new THREE.LatheGeometry(bottleShape().slice(0, 5), 40), liquidMat);
        liquid.scale.y = 0.001;
        liquid.position.y = 0;
        g.add(glass, liquid);
        bottleLine.add(g);
        bottles.push({ group: g, liquid, fill: 0 });
    }

    /* Water jet from pipe to bottles */
    const jetCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(1.15, -0.1, 0.5),
        new THREE.Vector3(0.6, -0.5, 0.75),
        new THREE.Vector3(0, -0.85, 0.85)
    ]);
    const jet = new THREE.Mesh(
        new THREE.TubeGeometry(jetCurve, 24, 0.035, 8, false),
        waterMat.clone()
    );
    jet.material.opacity = 0;
    machine.add(jet);

    /* ── Phase weights from scroll ── */
    function phase(p, a, b) {
        return clamp(0, 1, (p - a) / (b - a));
    }

    function updateScene(p, dt) {
        elapsed += dt;

        /* 0→0.28 waterfall | 0.22→0.48 clouds | 0.40→0.68 suction | 0.58→0.85 bottles */
        const fall = clamp(0, 1, 1 - phase(p, 0.2, 0.32));
        const gather = clamp(0, 1, phase(p, 0.2, 0.32) * (1 - phase(p, 0.52, 0.62)));
        const suck = clamp(0, 1, phase(p, 0.38, 0.48) * (1 - phase(p, 0.65, 0.75)));
        const fill = clamp(0, 1, phase(p, 0.55, 0.65));
        const showMachine = clamp(0, 1, phase(p, 0.34, 0.44));
        const showBottles = clamp(0, 1, phase(p, 0.52, 0.62));

        camera.position.y = lerp(0.5, -0.45, p);
        camera.position.z = lerp(5.2, 4.8, p);
        camera.lookAt(0, lerp(0, -0.35, p), 0);

        /* Waterfall streams */
        streams.forEach(s => {
            s.mesh.material.opacity = Math.max(0.15, fall * 0.95);
            s.mesh.visible = fall > 0.01 || p < 0.35;
        });
        pool.material.opacity = fall * 0.65 + gather * 0.3;

        /* Droplets */
        for (let i = 0; i < N; i++) {
            const d = dropState[i];
            const sx = streams[d.stream]?.x ?? 0;

            if (fall > 0.02 || p < 0.35) {
                d.y -= d.vy * (0.8 + fall * 1.2);
                d.x = sx + Math.sin(elapsed * 0.003 + d.phase) * 0.12;
            }

            /* Gather into clouds — droplets drift to cloud center and fade */
            if (gather > 0.05 && d.y < 0.5) {
                d.x = lerp(d.x, 0, gather * 0.04);
                d.y = lerp(d.y, -0.1 + Math.sin(d.phase) * 0.1, gather * 0.03);
            }

            /* Sucked into machine */
            if (suck > 0.05 && d.y < 1.5) {
                d.x = lerp(d.x, 0, suck * 0.06);
                d.y = lerp(d.y, 0.7, suck * 0.05);
                d.z = lerp(d.z, 0.5, suck * 0.04);
            }

            if (d.y < -0.8 || (suck > 0.8 && d.y > 0.5 && d.y < 0.9)) {
                d.y = 2.5 + Math.random();
                d.x = (Math.random() - 0.5) * 2.2;
            }

            const vis = Math.max(fall, p < 0.35 ? 0.7 : 0) * (1 - suck * 0.85);
            dummy.position.set(d.x, d.y, d.z);
            dummy.scale.setScalar(vis > 0.05 ? d.size : 0.001);
            dummy.updateMatrix();
            drops.setMatrixAt(i, dummy.matrix);
        }
        drops.instanceMatrix.needsUpdate = true;

        /* Clouds grow as water collects, shrink when sucked */
        cloudSprites.forEach((spr, i) => {
            const grow = gather * (0.4 + 0.6 * Math.sin(elapsed * 0.001 + spr.userData.seed));
            const shrink = suck;
            const scale = Math.max(0.01, grow * 2.2 * (1 - shrink * 0.95));
            spr.scale.set(scale * 1.6, scale, 1);
            spr.material.opacity = clamp(0, 1, grow * 0.85 * (1 - shrink * 0.98));

            if (suck > 0.1) {
                spr.position.x = lerp(spr.userData.bx, 0, suck * 0.035);
                spr.position.y = lerp(spr.userData.by, 0.65, suck * 0.035);
            } else {
                spr.position.x = spr.userData.bx + Math.sin(elapsed * 0.0008 + i) * 0.03;
                spr.position.y = spr.userData.by + Math.cos(elapsed * 0.0006 + i) * 0.02;
            }
        });

        /* Machine */
        machine.scale.setScalar(0.3 + showMachine * 0.7);
        machine.visible = showMachine > 0.05;
        fan.rotation.y += 0.06 + suck * 0.12 + fill * 0.04;

        spiralMat.opacity = suck * 0.85;
        const arr = spiralGeo.attributes.position.array;
        spiralState.forEach((s, i) => {
            if (suck > 0.08) {
                s.t -= s.speed * (0.5 + suck);
                if (s.t < 0) { s.t = 1; s.angle += 0.5; }
            }
            const r = (1 - s.t) * 1.4 * suck;
            const y = -0.5 + (1 - s.t) * 1.8;
            arr[i * 3] = Math.cos(s.angle + s.t * 8) * r;
            arr[i * 3 + 1] = y;
            arr[i * 3 + 2] = Math.sin(s.angle + s.t * 8) * r * 0.4;
        });
        spiralGeo.attributes.position.needsUpdate = true;

        /* Bottles fill */
        bottleLine.visible = showBottles > 0.05;
        bottleLine.scale.setScalar(0.4 + showBottles * 0.6);
        jet.material.opacity = fill * 0.85;
        bottles.forEach(b => {
            b.fill = Math.min(0.95, b.fill + fill * 0.018);
            b.liquid.scale.y = Math.max(0.001, b.fill);
        });

        /* UI */
        heroPanel?.classList.toggle('is-visible', p > 0.88);
        scrollIndicator?.classList.toggle('is-hidden', p > 0.08);
        document.body.classList.toggle('on-water-hero', p < 0.95);
    }

    function resize() {
        const w = canvas.clientWidth;
        const h = canvas.clientHeight;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }

    ScrollTrigger.create({
        trigger: storySection,
        start: 'top top',
        end: () => `+=${Math.round(innerHeight * 4.2)}`,
        scrub: reduced ? false : 0.5,
        pin: '.water-story-pin',
        anticipatePin: 1,
        invalidateOnRefresh: true,
        onUpdate: self => { progress = self.progress; }
    });

    resize();
    addEventListener('resize', resize);

    let last = performance.now();
    function loop(now) {
        const dt = now - last;
        last = now;
        updateScene(progress, dt);
        renderer.render(scene, camera);
        requestAnimationFrame(loop);
    }

    updateScene(0, 0);
    if (!reduced) requestAnimationFrame(loop);
    else renderer.render(scene, camera);

    window.waterCycleProgress = () => progress;
}

initWaterCycle();
