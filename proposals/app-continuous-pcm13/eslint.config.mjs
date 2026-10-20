import js from '@eslint/js';
import globals from 'globals';
import hooks from 'eslint-plugin-react-hooks';
import tseslint from 'typescript-eslint';

// Same TypeScript/browser/hooks rules as the App; this is a leaf-only check.
export default tseslint.config({
  files: ['**/*.ts', '**/*.tsx'],
  extends: [js.configs.recommended, ...tseslint.configs.recommended],
  languageOptions: {globals: globals.browser},
  plugins: {'react-hooks': hooks},
  rules: {
    ...hooks.configs.recommended.rules,
    'react-hooks/exhaustive-deps': 'error',
    '@typescript-eslint/no-unused-vars': ['error', {
      argsIgnorePattern: '^_', varsIgnorePattern: '^_', ignoreRestSiblings: true,
    }],
  },
});
