// Gruvbox Dark — Prism theme for prism-react-renderer
// Palette: https://github.com/morhetz/gruvbox

/** @type {import('prism-react-renderer').PrismTheme} */
const gruvboxDark = {
  plain: {
    color: '#ebdbb2',
    backgroundColor: '#282828',
  },
  styles: [
    {
      types: ['comment', 'prolog', 'doctype', 'cdata'],
      style: { color: '#928374', fontStyle: 'italic' },
    },
    {
      types: ['punctuation'],
      style: { color: '#bdae93' },
    },
    {
      types: ['namespace'],
      style: { opacity: 0.8 },
    },
    // Keywords: bright red
    {
      types: ['keyword', 'atrule'],
      style: { color: '#fb4934' },
    },
    // Strings: bright green
    {
      types: ['string', 'char', 'inserted', 'attr-value'],
      style: { color: '#b8bb26' },
    },
    // Numbers, booleans, constants: bright purple
    {
      types: ['number', 'boolean', 'constant', 'symbol', 'deleted', 'property'],
      style: { color: '#d3869b' },
    },
    // Functions, class names: bright yellow
    {
      types: ['function', 'class-name'],
      style: { color: '#fabd2f' },
    },
    // Tags (HTML/JSX): bright blue
    {
      types: ['tag'],
      style: { color: '#83a598' },
    },
    // Attributes, selectors, builtins: bright aqua
    {
      types: ['attr-name', 'selector', 'builtin'],
      style: { color: '#8ec07c' },
    },
    // Operators, URLs: bright orange
    {
      types: ['operator', 'entity', 'url', 'variable', 'regex', 'important'],
      style: { color: '#fe8019' },
    },
    {
      types: ['bold'],
      style: { fontWeight: 'bold' },
    },
    {
      types: ['italic'],
      style: { fontStyle: 'italic' },
    },
  ],
};

module.exports = gruvboxDark;
