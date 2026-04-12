// @ts-check
const { themes } = require('prism-react-renderer');
const gruvboxDark = require('./src/prismGruvboxDark');

const config = {
  title: 'RAG Cookbook',
  tagline: 'A structured curriculum for Python developers building RAG systems from first principles.',
  favicon: 'img/favicon.svg',
  url: 'https://soale2.github.io',
  baseUrl: '/RAG-Cookbook/',
  organizationName: 'soale2',
  projectName: 'RAG-Cookbook',
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
        path: 'foundations',
        routeBasePath: 'foundations',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'naive-rag',
        path: 'naive-rag',
        routeBasePath: 'naive-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'advanced-rag',
        path: 'advanced-rag',
        routeBasePath: 'advanced-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'agentic-rag',
        path: 'agentic-rag',
        routeBasePath: 'agentic-rag',
        sidebarPath: require.resolve('./sidebars.js'),
        exclude: ['**/*.py', '**/.gitkeep'],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'graph-rag',
        path: 'graph-rag',
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
          to: '/foundations',
          position: 'left',
        },
        {
          label: 'Tracks',
          position: 'left',
          items: [
            { label: 'Naive RAG', to: '/naive-rag' },
            { label: 'Advanced RAG', to: '/advanced-rag' },
            { label: 'Agentic RAG', to: '/agentic-rag' },
            { label: 'Graph RAG', to: '/graph-rag' },
          ],
        },
        {
          href: 'https://github.com/soale2/RAG-Cookbook',
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
            { label: 'Foundations', to: '/foundations' },
            { label: 'Naive RAG', to: '/naive-rag' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'Reference Implementations', to: '/foundations' },
            { label: 'Sample Papers', href: 'https://github.com/soale2/RAG-Cookbook/tree/main/data/papers' },
          ],
        },
        {
          title: 'Source',
          items: [
            { label: 'GitHub', href: 'https://github.com/soale2/RAG-Cookbook' },
          ],
        },
      ],
      copyright: `RAG Complete Study Guide. Open source curriculum.`,
    },
    prism: {
      theme: themes.github,
      darkTheme: gruvboxDark,
      additionalLanguages: ['python', 'bash'],
    },
  },
};

module.exports = config;
