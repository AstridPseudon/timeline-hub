import {useCurrentFrame} from 'remotion';
import type {ElementComponentProps} from '../../_shared/am';
import {amTypeDrawing} from './drawing';
import {prepareAmTypeCapability} from './scene-capability';

export default function AmType(props: ElementComponentProps) {
  return amTypeDrawing(props, useCurrentFrame());
}
// The selected registry forwards the declaration from this very drawing owner.
AmType.prepareSceneCapability = prepareAmTypeCapability;
