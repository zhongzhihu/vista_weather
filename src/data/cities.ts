// City data + forecast — used by the iPhone mockup.
// Photos are hot-linked from Unsplash for the prototype.
// For production, download them, place them in /public/cities/, and update the `photo` field.

export type Hour = {
  t: string;
  icon: "sun" | "cloud-sun" | "cloud" | "moon" | "cloud-night";
  v: number;
};

export type City = {
  id: string;
  name: string;
  region: string;
  caption: string;
  time: string;
  photo: string;
  hours: Hour[];
};

export const CITIES: Record<string, City> = {
  sf: {
    id: "sf",
    name: "San Francisco",
    region: "CA, United States",
    caption: "Golden Gate Bridge over the bay, sailboats catching the afternoon wind.",
    time: "4:57",
    photo: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=900&q=80&auto=format&fit=crop",
    hours: [
      { t: "11 AM", icon: "sun", v: 63 },
      { t: "12 PM", icon: "sun", v: 66 },
      { t: "1 PM",  icon: "sun", v: 66 },
      { t: "2 PM",  icon: "sun", v: 68 },
      { t: "3 PM",  icon: "sun", v: 70 },
    ],
  },
  paris: {
    id: "paris",
    name: "Paris",
    region: "Île-de-France, France",
    caption: "La Tour Eiffel au printemps, the iron lady framed in soft spring light.",
    time: "4:56",
    photo: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=900&q=80&auto=format&fit=crop",
    hours: [
      { t: "3 PM", icon: "cloud-sun", v: 58 },
      { t: "4 PM", icon: "cloud",     v: 59 },
      { t: "5 PM", icon: "cloud",     v: 59 },
      { t: "6 PM", icon: "cloud",     v: 57 },
      { t: "7 PM", icon: "cloud",     v: 55 },
    ],
  },
  yosemite: {
    id: "yosemite",
    name: "Yosemite",
    region: "CA, United States",
    caption: "North Dome rising above the valley pines as a river winds quietly below.",
    time: "4:57",
    photo: "https://images.unsplash.com/photo-1562310503-a918c4c61e38?w=900&q=80&auto=format&fit=crop",
    hours: [
      { t: "7 AM",  icon: "sun", v: 31 },
      { t: "8 AM",  icon: "sun", v: 33 },
      { t: "9 AM",  icon: "sun", v: 37 },
      { t: "10 AM", icon: "sun", v: 41 },
      { t: "11 AM", icon: "sun", v: 46 },
    ],
  },
};
