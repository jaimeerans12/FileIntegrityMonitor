# Sentinel-FIM: File Integrity Monitor

A security tool developed in Python to monitor and detect unauthorized modifications to a file system. This project demonstrates core concepts of the **Integrity** pillar in the CIA Triad.

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Security Objectives](#2-security-objectives)
3. [Technical Architecture](#3-technical-architecture)
    * 3.1 [Hashing Strategy (SHA-256)](#31-hashing-strategy-sha-256)
    * 3.2 [Data Persistence](#32-data-persistence)
4. [How It Works](#4-how-it-works)
    * 4.1 [Baseline Mode](#41-baseline-mode)
    * 4.2 [Monitor Mode](#42-monitor-mode)
5. [Logic Flowchart](#5-logic-flowchart)
6. [Challenges & Edge Cases](#6-challenges--edge-cases)
    * 6.1 [macOS System Files (.DS_Store)](#61-macos-system-files-ds_store)
    * 6.2 [Permission Handling](#62-permission-handling)
7. [Installation & Usage](#7-installation--usage)
8. [Future Roadmap](#8-future-roadmap)
9. [Author Info](#9-author-info)

---

## 1. Project Overview

## 2. Security Objectives
[Explain why File Integrity Monitoring is used in Product Security to catch malware or unauthorized configuration changes.]
