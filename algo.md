# Jumbled Frame Construction Algorithm

Last Updated: 2025-11-01 16:19:55 UTC  
Author: @BodanampatiMohith

## High-Level Architecture

```mermaid
flowchart TD
    subgraph Input
        A[Input Video File]
    end

    subgraph PreProcessing
        B[Frame Extraction]
        C[Frame Storage]
        D{Jumbling Required?}
        E[Frame Jumbling]
    end

    subgraph FeatureProcessing
        F[ResNet-18 Feature Extraction]
        G[Feature Vector Generation]
        H[Similarity Matrix Computation]
    end

    subgraph Optimization
        I[TSP Problem Formulation]
        J[Greedy Path Finding]
        K[Frame Order Generation]
    end

    subgraph VideoReconstruction
        L[Frame Assembly]
        M[Video Writer]
        N[Output Video]
    end

    A --> B
    B --> C
    C --> D
    D -->|Yes| E
    D -->|No| F
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N

