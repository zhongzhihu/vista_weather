import assert from "node:assert/strict";
import test from "node:test";
import region, { config } from "../netlify/edge-functions/region.js";
import { formatStormWindDetail, unitForCountryCode } from "../src/utils/wind-units.js";

test("uses mph in the United States and kmh in other countries or when unknown", () => {
  assert.equal(unitForCountryCode("US"), "mph");
  assert.equal(unitForCountryCode("us"), "mph");
  assert.equal(unitForCountryCode("GB"), "kmh");
  assert.equal(unitForCountryCode("CA"), "kmh");
  assert.equal(unitForCountryCode(null), "kmh");
});

test("formats storm wind speeds in mph or rounded kmh", () => {
  const storm = { maxWindMph: 120, direction: "N", movingSpeedMph: 17 };

  assert.equal(
    formatStormWindDetail(storm, "mph"),
    "Max winds 120 mph · Moving N at 17 mph",
  );
  assert.equal(
    formatStormWindDetail(storm, "kmh"),
    "Max winds 200 kmh · Moving N at 30 kmh",
  );
  assert.equal(
    formatStormWindDetail({ maxWindMph: 100, direction: "NW", movingSpeedMph: 2 }, "kmh"),
    "Max winds 160 kmh · Moving NW at 5 kmh",
  );
  assert.equal(
    formatStormWindDetail({ maxWindMph: 50, direction: "NE", movingSpeedMph: 5 }, "kmh"),
    "Max winds 80 kmh · Moving NE at 10 kmh",
  );
});

test("Netlify region endpoint exposes only a normalized country code to the site", async () => {
  assert.equal(config.path, "/api/region");

  const request = new Request("https://vistaweather.com/api/region", {
    headers: { origin: "https://zhongzhihu.github.io" },
  });
  const response = await region(request, {
    geo: { country: { code: "us" } },
    ip: "192.0.2.1",
  });

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { countryCode: "US" });
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.equal(response.headers.get("access-control-allow-origin"), "https://zhongzhihu.github.io");
});

test("region endpoint uses a metric-safe fallback when Netlify has no country", async () => {
  const request = new Request("https://vistaweather.com/api/region", {
    headers: { origin: "https://vistaweather.com" },
  });
  const response = await region(request, { geo: { country: {} } });

  assert.deepEqual(await response.json(), { countryCode: null });
});
