import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://vistaweather.com",
  compressHTML: true,
  devToolbar: {
    enabled: false,
  },
  integrations: [sitemap()],
});
