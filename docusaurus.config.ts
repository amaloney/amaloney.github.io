import {themes as prismThemes} from 'prism-react-renderer'
import type {Config} from '@docusaurus/types'
import type * as Preset from '@docusaurus/preset-classic'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'

const config: Config = {
    title: 'Andy Maloney',
    tagline: '',
    favicon: 'img/favicon.ico',

    url: 'https://amaloney.github.io',
    baseUrl: '/',
    projectName: 'amaloney.github.io',
    organizationName: 'amaloney',
    trailingSlash: true,

    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',

    i18n: {
        defaultLocale: 'en',
        locales: ['en'],
    },

    presets: [
        [
            'classic',
            {
                docs: {
                    sidebarPath: './sidebars.ts',
                },
                blog: {
                    showReadingTime: true,
                    feedOptions: {
                        type: ['rss', 'atom'],
                        xslt: true,
                    },
                    // Useful options to enforce blogging best practices
                    onInlineTags: 'warn',
                    onInlineAuthors: 'warn',
                    onUntruncatedBlogPosts: 'warn',
                    remarkPlugins: [remarkMath],
                    rehypePlugins: [rehypeKatex],
                },
                theme: {
                    customCss: './src/css/custom.css',
                },
            } satisfies Preset.Options,
        ],
    ],

    themeConfig: {
        // Replace with your project's social card
        image: 'img/docusaurus-social-card.jpg',
        navbar: {
            title: '',
            logo: {
                alt: 'logo',
                src: 'img/logo.svg',
            },
            items: [
                {
                    type: 'docSidebar',
                    sidebarId: 'projectsSidebar',
                    position: 'left',
                    label: 'Projects',
                },
                {to: '/blog', label: 'Blog', position: 'left'},
                {
                    href: 'https://github.com/amaloney',
                    label: 'GitHub',
                    position: 'right',
                },
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: 'Docs',
                    items: [
                        {
                            label: 'Tutorial',
                            to: '/docs/intro',
                        },
                    ],
                },
                {
                    title: 'Community',
                    items: [],
                },
                {
                    title: 'More',
                    items: [
                        {
                            label: 'Blog',
                            to: '/blog',
                        },
                        {
                            label: 'GitHub',
                            href: 'https://github.com/amaloney',
                        },
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} Andy Maloney. Built with Docusaurus.`,
        },
        prism: {
            theme: prismThemes.duotoneLight,
            darkTheme: prismThemes.duotoneDark,
        },
    } satisfies Preset.ThemeConfig,
}

export default config
