// @ts-check
const { themes } = require('prism-react-renderer');

const config = {
  title: 'RAG Complete Study Guide',
  tagline: 'A structured curriculum for Python developers building RAG systems from first principles.',
  favicon: 'img/favicon.svg',
  url: 'https://soale2.github.io',
  baseUrl: '/RAG-Complete-Study-Guide/',
  organizationName: 'soale2',
  projectName: 'RAG-Complete-Study-Guide',
  trailingSlash: false,

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: false,
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'foundations',
        path: '../foundations',
        routeBasePath: 'foundations',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'naive-rag',
        path: '../naive-rag',
        routeBasePath: 'naive-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'advanced-rag',
        path: '../advanced-rag',
        routeBasePath: 'advanced-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'agentic-rag',
        path: '../agentic-rag',
        routeBasePath: 'agentic-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'graph-rag',
        path: '../graph-rag',
        routeBasePath: 'graph-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'RAG Study Guide',
      items: [
        {
          label: 'Foundations',
          to: '/foundations/README',
          position: 'left',
        },
        {
          label: 'Tracks',
          position: 'left',
          items: [
            { label: 'Naive RAG', to: '/naive-rag/README' },
            { label: 'Advanced RAG', to: '/advanced-rag/README' },
            { label: 'Agentic RAG', to: '/agentic-rag/README' },
            { label: 'Graph RAG', to: '/graph-rag/README' },
          ],
        },
        {
          href: 'https://github.com/soale2/RAG-Complete-Study-Guide',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'Curriculum',
          items: [
            { label: 'Foundations', to: '/foundations/README' },
            { label: 'Naive RAG', to: '/naive-rag/README' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'Reference Implementations', to: '/foundations/README' },
            { label: 'Sample Papers', href: 'https://github.com/soale2/RAG-Complete-Study-Guide/tree/main/data/papers' },
          ],
        },
        {
          title: 'Source',
          items: [
            { label: 'GitHub', href: 'https://github.com/soale2/RAG-Complete-Study-Guide' },
          ],
        },
      ],
      copyright: `RAG Complete Study Guide — open source curriculum.`,
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'bash'],
    },
  },
};

module.exports = config;
