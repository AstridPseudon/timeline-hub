export interface CodePathPreviewAsset {key:string;url:string;}
export interface CodePathPreviewProps {code:string;defaultsJson:object;fps?:number;allowedAssets?:readonly CodePathPreviewAsset[];}
/** Saved resource code is migration data; only admitted pack components execute in the editor. */
export function CodePathPreview(_props:CodePathPreviewProps){
  return <div role="status" className="rounded-lg border border-border bg-muted/30 p-3 text-sm text-muted-foreground">Custom component preview requires an admitted project pack. Saved source is preserved for migration.</div>;
}
