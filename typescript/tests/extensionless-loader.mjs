export async function resolve(specifier, context, nextResolve) {
  if ((specifier.startsWith('./') || specifier.startsWith('../'))
      && !specifier.endsWith('.js')) {
    try {
      return await nextResolve(`${specifier}.js`, context);
    } catch {
      // Let Node produce its normal diagnostic for unresolved imports.
    }
  }
  return nextResolve(specifier, context);
}
