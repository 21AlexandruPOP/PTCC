Pentru a ajunge la versiunea curenta, am experimentat.

Am efectuat 4 experimente sistematice pentru a determina configurația optimă a rețelei neuronale pentru predicția consumului.

### Experiment 1: Baseline
- **Configurație:** Layers (64, 32), Batch 200, Epochs 200.
- **Observație:** Modelul a fost prea complex pentru volumul de date, iar limita de 200 de epoci a oprit invatarea prematur.

### Experiment 2: Ajustare Arhitectura
- **Configurație:** Layers (32, 16), Batch 200, Epochs 2000.
- **Observație:** Reducerea complexității straturilor a îmbunătățit generalizarea. Modelul a convergit la epoca 450. **MAE cam pe la 0.56**

### Experiment 3: Optimizare Batch 
- **Configurație:** Layers (32, 16), Batch 32, Epochs 2000.
- **Observație:** Un batch mai mic (32) a permis optimizer-ului Adam sa faca reglaje mai fine. **MAE a scăzut la 0.47 litri.**

### Experiment 4: Testare Stabilitate
- **Configurație:** Layers (32, 16), Batch 32, Learning Rate 0.01.
- **Observație:** Un pas de invatare prea mare a dus la instabilitatea pierderii (loss-ului), modelul sarind peste minimul local.