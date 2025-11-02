# Eddy WanVideo Cinematic TextEncode

Author: eddy

Αυτόνομος κόμβος WanVideo TextEncode με ενσωματωμένους κινηματογραφικούς και κινήσεις κάμερας ελέγχους.
Παρέχει προεπιθέματα προτροπής, επανακωδικοποίηση T5 και πλήρη συμβατότητα με τη ροή WanVideo.

## Χαρακτηριστικά

**Κόμβος «Όλα-σε-Ένα» για TextEncode:**
- Αντικαθιστά λειτουργικά τον αρχικό WanVideoTextEncode χωρίς να τον τροποποιεί
- Ενσωματωμένοι έλεγχοι κινηματογραφίας (χρόνος, φωτισμός, χρωματική τονικότητα, μέγεθος πλάνου, γωνία λήψης, σύνθεση)
- Ενσωματωμένοι έλεγχοι κίνησης κάμερας (pan, tilt, dolly, crane, orbit, tracking, zoom, roll)
- Ενσωματωμένοι έλεγχοι αισθητικής (color grading, lighting style, lens style, film stock, color palette)
- Ενσωματωμένοι έλεγχοι οπτικού στυλ (visual style: anime, realistic, 2.5D, Chinese style, pixel art κ.ά.)
- Επεκταμένοι έλεγχοι φωτισμού (40 επιλογές: rembrandt, golden hour, three-point, rim light κ.ά.)
- 16 κατηγορίες ελέγχου με 127 επιλογές συνολικά
- Αυτόματη προσθήκη επιλεγμένων όρων πριν από την κύρια προτροπή
- Υποστήριξη των αρχικών δυνατοτήτων: prompt travel (|), EchoShot ([1]), συντακτικό βαρών (text:1.5)
- Υποστήριξη προσωρινής μνήμης στον δίσκο

## Χρήση

### Βασική ροή εργασίας

```
LoadWanVideoT5TextEncoder
  ↓ t5
Eddy WanVideo TextEncode (Cinematic)
  ↓ text_embeds
WanVideoSampler
```

### Παράμετροι

**Απαιτούμενα:**
- `positive_prompt`: Η κύρια προτροπή
- `negative_prompt`: Αρνητική προτροπή
- `t5`: Ο T5 encoder από τον LoadWanVideoT5TextEncoder (προαιρετικός όταν χρησιμοποιείται cache)

**Προαιρετικοί Κινηματογραφικοί Έλεγχοι:**
- `enable_cinematic`: Ενεργοποίηση/Απενεργοποίηση (προεπιλογή: true)
- `visual_style`: photorealistic/anime/cel-shaded/2.5D/Chinese style/pixel art/3D game κ.ά. (19 επιλογές)
- `time`: Day/Night/Dawn/Sunrise
- `light_source`: Daylight/Artificial/Moonlight/Fire κ.ά. (8 επιλογές)
- `light_intensity`: Soft/Hard/Diffused/Dramatic/Ambient/Contrasty lighting (6 επιλογές)
- `light_angle`: Top/Side/Under/Edge lighting (4 επιλογές)
- `color_tone`: Warm/Cool/Mixed colors
- `shot_size`: Medium/Close-up/Wide/Extreme shots
- `camera_angle`: Over-the-shoulder/Low/High/Dutch/Aerial/Overhead
- `composition`: Center/Balanced/Left-heavy/Right-heavy/Symmetrical
- `camera_motion`: static/pan/tilt/dolly/crane/orbit/tracking/zoom/roll (23 επιλογές)
- `color_grading`: teal-and-orange/bleach-bypass/kodak portra
- `lighting_style`: rembrandt/golden hour/blue hour/three-point/backlighting κ.ά. (16 επιλογές)
- `lighting_technique`: key light/fill light/rim light/hair light κ.ά. (6 επιλογές)
- `lens_style`: anamorphic bokeh/16mm grain/CGI stylized
- `film_stock`: Kodak Vision3 500T/Cinestill 800T/Fuji Eterna κ.ά. (6 επιλογές)
- `color_palette`: high-contrast/low-contrast/pastel tones/monochrome κ.ά. (8 επιλογές)

**Λοιπά:**
- `force_offload`: Μεταφορά του T5 σε CPU μετά την κωδικοποίηση (προεπιλογή: true)
- `use_disk_cache`: Αποθήκευση embeddings στον δίσκο (προεπιλογή: false)
- `device`: gpu/cpu

## Πώς λειτουργεί

Όταν `enable_cinematic` είναι ενεργό:
1. Συλλέγει όλους τους επιλεγμένους όρους (αγνοεί το "none")
2. Τους συνενώνει με κόμματα
3. Τους προσαρτά πριν από την κύρια προτροπή
4. Κωδικοποιεί το τελικό κείμενο με τον T5

Αποτέλεσμα: Ο sampler λαμβάνει embeddings με ενσωματωμένη την κινηματογραφική αισθητική.

## Συμβουλές

- Θέστε `camera_angle` σε "none" αν η προτροπή ήδη περιγράφει κίνηση (σύμφωνα με τις οδηγίες WanVideo 2.2)
- Παρέχονται επίσης:
  - Prompt travel: `"scene1 | scene2 | scene3"`
  - EchoShot: `"shot1 [1] shot2 [2] shot3"`
  - Βάρη: `"(beautiful:1.5) girl (sunset:0.8)"`
- Απενεργοποιήστε τους κινηματογραφικούς όρους με `enable_cinematic=false` για πλήρη χειροκίνητο έλεγχο

## Εγκατάσταση

1. Τοποθετήστε τον φάκελο στο `ComfyUI/custom_nodes/`
2. Επανεκκινήστε το ComfyUI ή επιλέξτε "Reload Custom Nodes"
3. Βρείτε τον κόμβο στην κατηγορία "EddyWanCon": "Eddy WanVideo TextEncode (Cinematic)"

## Σύγκριση με τον αρχικό κόμβο

| Λειτουργία | Αρχικός | Eddy Cinematic |
|------------|---------|----------------|
| Βασική κωδικοποίηση | Ναι | Ναι |
| Prompt travel \| | Ναι | Ναι |
| EchoShot [1] | Ναι | Ναι |
| Συντακτικό βαρών | Ναι | Ναι |
| Cache δίσκου | Ναι | Ναι |
| Κινηματογραφικοί έλεγχοι (9 κατηγορίες) | Όχι | Ναι (ενσωματωμένοι) |
| Έλεγχοι κίνησης κάμερας (23 επιλογές) | Όχι | Ναι (ενσωματωμένοι) |
| Έλεγχοι αισθητικής (6 κατηγορίες, 29 επιλογές) | Όχι | Ναι (ενσωματωμένοι) |
| Έλεγχοι οπτικού στυλ (19 επιλογές) | Όχι | Ναι (ενσωματωμένοι) |
| Έλεγχοι φωτισμού (40 επιλογές συνολικά) | Όχι | Ναι (επεκταμένοι) |
| Σύνολο επιλογών ελέγχου | 0 | 127 |
| Απαιτούνται ξεχωριστά prefix nodes | Όχι | Όχι |

## Σημειώσεις

- Αυτός είναι **αυτόνομος** κόμβος· δεν τροποποιεί το WanVideoWrapper
- Βασισμένος στις επίσημες οδηγίες κινηματογραφίας WanVideo 2.2 A14B
- Οι όροι κινηματογραφίας είναι στα Αγγλικά (συμβατοί με τις επίσημες προδιαγραφές)
- Λειτουργεί με όλα τα μοντέλα WanVideo (A14B, 5B, I2V, T2V, κ.ά.)
- Επεκταμένοι έλεγχοι φωτισμού βασισμένοι σε επαγγελματικές τεχνικές κινηματογραφίας
  - Rembrandt lighting, Three-point lighting, Golden/Blue hour
  - Key light, Fill light, Rim light, Hair light
  - Πηγές: Wan 2.2 επίσημη τεκμηρίωση + MimicPC 69+ παραδείγματα + επαγγελματικά πρότυπα

## Παραδείγματα προτροπών

**Χωρίς κινηματογραφία (enable_cinematic=false):**
```
A girl walking in the park
```

**Με κινηματογραφία (βασική):**
```
时间：Day time, 光源：Daylight, 光线强度：Soft lighting, 光线角度：Side lighting, 色调：Warm colors, 镜头尺寸：Medium shot, 构图：Center composition, A girl walking in the park
```

**Με κίνηση κάμερας:**
```
时间：Day time, 光源：Daylight, 运镜：dolly in, A girl walking in the park
```

**Με πλήρη αισθητική ελέγχους:**
```
时间：Night time, 光源：Moonlight, 运镜：dolly in, 调色：teal-and-orange, 光照风格：neon rim light, 镜头风格：anamorphic bokeh, 胶片：Kodak Vision3 500T, 色彩母题：low-contrast, A cinematic shot of a cyberpunk city
```

**Με προηγμένους ελέγχους φωτισμού:**
```
时间：Night time, 光源：Moonlight, 光线强度：Dramatic lighting, 光照风格：rembrandt lighting, 打光技术：rim light, 运镜：dolly in, 调色：teal-and-orange, A moody portrait of a detective
```

**Με οπτικό στυλ (Νέο!):**
```
视觉风格：anime style, 时间：Night time, 光源：Moonlight, 运镜：dolly in, A magical girl fighting in the city
```

```
视觉风格：Chinese style, 时间：Day time, 光源：Daylight, 运镜：crane up, A traditional Chinese garden with cherry blossoms
```

```
视觉风格：photorealistic, 时间：Golden hour, 光源：Daylight, 光照风格：golden hour, 运镜：dolly in, A fashion model walking on the street
```

Ο κόμβος προσθέτει αυτόματα τα προεπιθέματα· εσείς γράφετε μόνο την κύρια προτροπή.
