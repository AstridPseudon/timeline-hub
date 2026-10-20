// Pure camera maths for the World Explorer. No three.js, no dependencies.
// Conventions: Y-up, right-handed; camera at identity looks down -Z.
// Yaw turns about +Y (positive turns left); pitch turns about the camera's local X (positive looks up).
import type { Vec3, Quat } from '../runtime';

export const MAX_PITCH = (89 * Math.PI) / 180;

const TWO_PI = Math.PI * 2;
const MAX_DT = 0.1;

export type Bounds = { readonly min: Vec3; readonly max: Vec3 };
export type MoveInput = { forward: number; right: number; up: number };
export type ViewPose = {
  position: [number, number, number];
  quaternion: [number, number, number, number];
  fov: number;
};

// ---- vec3 helpers -------------------------------------------------------

export function vadd(a: Vec3, b: Vec3): [number, number, number] {
  return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
}

export function vsub(a: Vec3, b: Vec3): [number, number, number] {
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

export function vscale(a: Vec3, s: number): [number, number, number] {
  return [a[0] * s, a[1] * s, a[2] * s];
}

export function vdot(a: Vec3, b: Vec3): number {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

export function vcross(a: Vec3, b: Vec3): [number, number, number] {
  return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
}

export function vlength(a: Vec3): number {
  return Math.sqrt(vdot(a, a));
}

export function vnormalize(a: Vec3): [number, number, number] {
  const len = vlength(a);
  return len > 0 ? vscale(a, 1 / len) : [0, 0, 0];
}

// ---- angles and orientation --------------------------------------------

export function clampPitch(p: number): number {
  return Math.min(MAX_PITCH, Math.max(-MAX_PITCH, p));
}

// Wraps an angle into (-PI, PI].
function wrapYaw(a: number): number {
  let y = a % TWO_PI;
  if (y <= -Math.PI) y += TWO_PI;
  if (y > Math.PI) y -= TWO_PI;
  return y;
}

export function forwardFromYawPitch(yaw: number, pitch: number): Vec3 {
  return [-Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch)];
}

type Q4 = [number, number, number, number];

// Hamilton product a * b, quaternions stored as [x, y, z, w].
function qmul(a: Q4, b: Q4): Q4 {
  const [ax, ay, az, aw] = a;
  const [bx, by, bz, bw] = b;
  return [
    aw * bx + ax * bw + ay * bz - az * by,
    aw * by - ax * bz + ay * bw + az * bx,
    aw * bz + ax * by - ay * bx + az * bw,
    aw * bw - ax * bx - ay * by - az * bz,
  ];
}

export function quatFromYawPitch(yaw: number, pitch: number): Quat {
  const qYaw: Q4 = [0, Math.sin(yaw / 2), 0, Math.cos(yaw / 2)];
  const qPitch: Q4 = [Math.sin(pitch / 2), 0, 0, Math.cos(pitch / 2)];
  const [x, y, z, w] = qmul(qYaw, qPitch);
  return [x, y, z, w];
}

// Rotates v by the unit quaternion q: v' = q v q*.
export function quatRotate(q: Quat, v: Vec3): [number, number, number] {
  const u: Vec3 = [q[0], q[1], q[2]];
  const t = vscale(vcross(u, v), 2);
  const withT = vadd(v, vscale(t, q[3]));
  return vadd(withT, vcross(u, t));
}

export function yawPitchFromDirection(dir: Vec3): { yaw: number; pitch: number } {
  const n = vnormalize(dir);
  if (n[0] === 0 && n[1] === 0 && n[2] === 0) return { yaw: 0, pitch: 0 };
  const pitch = clampPitch(Math.asin(Math.min(1, Math.max(-1, n[1]))));
  const horizontal = Math.hypot(n[0], n[2]);
  // Straight up or down has no defined yaw; use 0.
  const yaw = horizontal < 1e-12 ? 0 : Math.atan2(-n[0], -n[2]);
  return { yaw, pitch };
}

export function yawPitchLookAt(position: Vec3, target: Vec3): { yaw: number; pitch: number } {
  return yawPitchFromDirection(vsub(target, position));
}

// ---- bounds and speed --------------------------------------------------

export function clampToBounds(p: Vec3, bounds?: Bounds): [number, number, number] {
  if (!bounds) return [p[0], p[1], p[2]];
  const out: [number, number, number] = [p[0], p[1], p[2]];
  for (let i = 0; i < 3; i++) {
    out[i] = Math.min(bounds.max[i], Math.max(bounds.min[i], out[i]));
  }
  return out;
}

export function defaultExploreSpeed(bounds?: Bounds): number {
  if (!bounds) return 4;
  const extent = Math.max(
    bounds.max[0] - bounds.min[0],
    bounds.max[1] - bounds.min[1],
    bounds.max[2] - bounds.min[2],
  );
  return Math.max(0.01, extent / 8);
}

// ---- free camera -------------------------------------------------------

const finite = (n: number) => Number.isFinite(n);

function sanitizeAxis(n: number): number {
  return finite(n) ? Math.min(1, Math.max(-1, n)) : 0;
}

export class FreeCamera {
  private _position: [number, number, number];
  private _yaw: number;
  private _pitch: number;
  private _version = 0;
  private readonly bounds?: Bounds;
  private readonly start: { position: [number, number, number]; yaw: number; pitch: number };

  constructor(start: { position: Vec3; target: Vec3 }, bounds?: Bounds) {
    this.bounds = bounds;
    const position = clampToBounds(start.position, bounds);
    const { yaw, pitch } = yawPitchLookAt(position, start.target);
    this.start = { position, yaw, pitch };
    this._position = [position[0], position[1], position[2]];
    this._yaw = yaw;
    this._pitch = pitch;
  }

  get position(): Vec3 {
    return this._position;
  }

  get yaw(): number {
    return this._yaw;
  }

  get pitch(): number {
    return this._pitch;
  }

  get version(): number {
    return this._version;
  }

  reset(): void {
    this.setState(this.start.position, this.start.yaw, this.start.pitch);
  }

  look(dYaw: number, dPitch: number): void {
    if (!finite(dYaw) || !finite(dPitch)) return;
    this.setState(this._position, wrapYaw(this._yaw + dYaw), clampPitch(this._pitch + dPitch));
  }

  move(input: MoveInput, speed: number, dt: number): void {
    const step = finite(dt) ? Math.min(MAX_DT, Math.max(0, dt)) : 0;
    const distance = (finite(speed) ? speed : 0) * step;
    let f = sanitizeAxis(input.forward);
    let r = sanitizeAxis(input.right);
    let u = sanitizeAxis(input.up);
    const len = Math.hypot(f, r, u);
    if (len > 1) {
      f /= len;
      r /= len;
      u /= len;
    }
    this.translate(r * distance, u * distance, f * distance);
  }

  translate(right: number, up: number, forward: number): void {
    if (!finite(right) || !finite(up) || !finite(forward)) return;
    const fwd = forwardFromYawPitch(this._yaw, this._pitch);
    const rightVec: Vec3 = [Math.cos(this._yaw), 0, -Math.sin(this._yaw)];
    const delta = vadd(
      vadd(vscale(rightVec, right), [0, up, 0]),
      vscale(fwd, forward),
    );
    this.setState(clampToBounds(vadd(this._position, delta), this.bounds), this._yaw, this._pitch);
  }

  pose(fov: number): ViewPose {
    const [qx, qy, qz, qw] = quatFromYawPitch(this._yaw, this._pitch);
    return {
      position: [this._position[0], this._position[1], this._position[2]],
      quaternion: [qx, qy, qz, qw],
      fov,
    };
  }

  private setState(position: Vec3, yaw: number, pitch: number): void {
    const changed =
      position[0] !== this._position[0] ||
      position[1] !== this._position[1] ||
      position[2] !== this._position[2] ||
      yaw !== this._yaw ||
      pitch !== this._pitch;
    if (!changed) return;
    this._position = [position[0], position[1], position[2]];
    this._yaw = yaw;
    this._pitch = pitch;
    this._version += 1;
  }
}
