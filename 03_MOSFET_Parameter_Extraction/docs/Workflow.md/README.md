# Workflow

The toolkit follows a systematic parameter extraction workflow.

```
LTspice Simulation
        │
        ▼
Data Import
        │
        ▼
Parameter Extraction
        │
        ▼
Parameter Verification
        │
        ▼
Visualization
        │
        ▼
Compact Model Evaluation
```

---

## Description

### 1. LTspice Simulation

Generate MOSFET I–V characteristics.

### 2. Data Import

Import simulation data into MATLAB.

### 3. Parameter Extraction

Extract Level-1 model parameters.

### 4. Verification

Evaluate extraction accuracy under different bias conditions.

### 5. Visualization

Generate comparison plots and error distributions.

### 6. Model Evaluation

Assess model accuracy and parameter consistency.
