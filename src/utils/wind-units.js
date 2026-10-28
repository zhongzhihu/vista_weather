const KILOMETERS_PER_MILE = 1.609344;

/**
 * Vista Weather defaults to mph in the United States and km/h elsewhere.
 * Visitors can override this choice in the wind units menu.
 *
 * @param {string | null | undefined} countryCode
 * @returns {"mph" | "kmh"}
 */
export function unitForCountryCode(countryCode) {
  return String(countryCode ?? "").trim().toUpperCase() === "US" ? "mph" : "kmh";
}

/**
 * @param {number} speedMph
 * @param {"mph" | "kmh"} unit
 */
function formatSpeed(speedMph, unit) {
  const speed = unit === "mph" ? Math.round(speedMph) : Math.round(speedMph * KILOMETERS_PER_MILE);
  return `${speed} ${unit === "mph" ? "mph" : "km/h"}`;
}

/**
 * @param {{ maxWindMph: number, direction: string, movingSpeedMph: number }} storm
 * @param {"mph" | "kmh"} unit
 */
export function formatStormWindDetail(storm, unit) {
  return `Max winds ${formatSpeed(storm.maxWindMph, unit)} · Moving ${storm.direction} at ${formatSpeed(storm.movingSpeedMph, unit)}`;
}
