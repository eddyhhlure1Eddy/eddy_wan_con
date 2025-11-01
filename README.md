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
- 14 κατηγορίες ελέγχου με 85 επιλογές συνολικά
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
- `time`: Day/Night/Dawn/Sunrise
- `light_source`: Daylight/Artificial/Moonlight/Fire κ.ά.
- `light_intensity`: Soft/Hard lighting
- `light_angle`: Top/Side/Under/Edge lighting
- `color_tone`: Warm/Cool/Mixed colors
- `shot_size`: Medium/Close-up/Wide/Extreme shots
- `camera_angle`: Over-the-shoulder/Low/High/Dutch/Aerial/Overhead
- `composition`: Center/Balanced/Left-heavy/Right-heavy/Symmetrical
- `camera_motion`: static/pan/tilt/dolly/crane/orbit/tracking/zoom/roll
- `color_grading`: teal-and-orange/bleach-bypass/kodak portra
- `lighting_style`: volumetric dusk/harsh noon sun/neon rim light
- `lens_style`: anamorphic bokeh/16mm grain/CGI stylized
- `film_stock`: Kodak Vision3 500T/Cinestill 800T/Fuji Eterna κ.ά.
- `color_palette`: high-contrast/low-contrast/pastel tones/monochrome κ.ά.

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
| Έλεγχοι αισθητικής (5 κατηγορίες, 23 επιλογές) | Όχι | Ναι (ενσωματωμένοι) |
| Σύνολο επιλογών ελέγχου | 0 | 85 |
| Απαιτούνται ξεχωριστά prefix nodes | Όχι | Όχι |

## Σημειώσεις

- Αυτός είναι **αυτόνομος** κόμβος· δεν τροποποιεί το WanVideoWrapper
- Βασισμένος στις επίσημες οδηγίες κινηματογραφίας WanVideo 2.2 A14B
- Οι όροι κινηματογραφίας είναι στα Αγγλικά (συμβατοί με τις επίσημες προδιαγραφές)
- Λειτουργεί με όλα τα μοντέλα WanVideo (A14B, 5B, I2V, T2V, κ.ά.)

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

Ο κόμβος προσθέτει αυτόματα τα προεπιθέματα· εσείς γράφετε μόνο την κύρια προτροπή.
