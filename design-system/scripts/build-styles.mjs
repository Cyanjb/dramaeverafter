// Concatenates the brand font import with the site's real style.css into
// dist/styles.css. The site stylesheet is the single source of truth for the
// design system's look; this runs on every build so the copy can never go stale.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const pkgRoot = join(here, '..');
const siteCss = readFileSync(join(pkgRoot, '..', 'style.css'), 'utf8');

const fonts = `@import url("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap");\n`;

mkdirSync(join(pkgRoot, 'dist'), { recursive: true });
writeFileSync(join(pkgRoot, 'dist', 'styles.css'), fonts + siteCss);
console.log('dist/styles.css written (%d bytes site css)', siteCss.length);
