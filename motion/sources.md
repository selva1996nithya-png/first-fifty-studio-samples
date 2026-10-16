# A higher starting point

Original 26-second, 1080×1350, 24 fps animated infographic for TaskMarket TSK-BYW11CAS. Prepared 16 October 2026 UTC.

## Fact checks

- **Kelvin waves temporarily raise coastal sea levels; they are not tsunamis.** SFist, 5 October 2026: [SF Braces for Unusually High Tides as El Niño Sends ‘Kelvin Waves’ Toward the Coast](https://sfist.com/2026/10/05/sf-braces-for-unusually-high-tides-as-el-nino-sends-kelvin-waves-toward-the-coast/). The report explains that the extra water can worsen flooding and erosion when it overlaps a high tide or storm.
- **San Francisco tides approximately six inches above normal.** The same dated SFist report attributes this observation to Mayor Lurie's public video. This is a reported local observation, not a coast-wide forecast or an independently measured value.
- **King tides peak November–February.** The same SFist report gives this period. It does not imply continuously flooded streets or a single predicted flood height.
- **Strong-to-very strong El Niño likely through January–March 2027.** [NOAA Climate Prediction Center ENSO Diagnostic Discussion, issued 8 October 2026](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso_advisory/ensodisc.shtml). This is an ENSO outlook, not a promise of a particular local flood outcome.

Every numerical claim in the animation carries a visible [1] SFist or [2] NOAA source tag. The date of each source appears throughout. The water and street drawing is explicitly schematic and not to scale. Its movement communicates overlapping effects; it is not a flood simulation or a tide-height projection. The final statement about a smaller margin is an explanatory inference from the sourced overlap mechanism.

## Production and delivery

The animation was made with deterministic Python drawing and explicitly coded motion. AI assistance was used to write the code and research the sources. No generative video model, stock footage, third-party illustration or fabricated footage was used. The requester can evaluate whether this production method meets the brief's “hand-made motion, no AI video” requirement. No human manual production is claimed.

`render.py` is editable source. It uses Pillow, the freely distributed DejaVu Sans typeface and an FFmpeg binary supplied by imageio-ffmpeg. `higher-baseline.mp4` is the final H.264 MP4, without audio. The contact sheet and four PNG frames are review previews, not additional entries.

Pitch: A street-edge diagram shows the hidden problem: a temporarily higher coastal baseline leaves less room for the next high tide. The final winter timeline distinguishes the ENSO outlook from the local king-tide season, without presenting the schematic as a numerical forecast.
