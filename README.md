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

**Sentinel-FIM** is a lightweight File Integrity Monitor (FIM) built in Python. This tool is designed to serve as a security utility that snapshots the "state" of a local directory and alerts the user to any unauthorized changes. 

In the context of **Product Security**, maintaining the integrity of source code and configuration files is paramount. This project demonstrates how automated auditing can detect the early stages of a system compromise, such as the injection of a backdoor or the modification of sensitive environment variables.

### The Problem
When a system is breached, attackers often modify existing files or drop malicious scripts into the file system. Without an automated integrity check, these changes can go unnoticed for months. Manual verification is impossible for large-scale projects, creating a need for a programmatic "source of truth."

### The Solution
Sentinel-FIM solves this by utilizing cryptographic hashing to create a unique "fingerprint" for every file within a target folder. By comparing these fingerprints over time, the tool can precisely identify:
* **Integrity Violations:** Existing files that have been modified (even by a single bit).
* **Unauthorized Additions:** New, unknown files that have appeared in the directory.
* **Data Loss:** Files that were present in the baseline but have since been deleted.

### Target Environment
While cross-platform by design, this tool was developed and tested on **macOS**, focusing on handling Unix-based file structures and system-specific edge cases (such as handling `.DS_Store` metadata files).

## 2. Security Objectives

The development of Sentinel-FIM is centered around the **CIA Triad** (Confidentiality, Integrity, and Availability), specifically focusing on the **Integrity** pillar. The project aims to achieve the following security goals:

### 🛡️ Data Integrity Verification
The primary objective is to ensure that "Data at Rest" has not been tampered with. By using cryptographic hashes, the tool provides a mathematical guarantee that a file's content is identical to its original "known-good" state.

### 🔍 Detection of "Living off the Land" Attacks
Modern attackers often use legitimate system tools or modify existing scripts to stay hidden. Sentinel-FIM is designed to detect these subtle changes in source code or configuration files that traditional antivirus or signature-based scanners might overlook.

### 📉 Reducing Mean Time to Detect (MTTD)
In security engineering, the goal is to discover a breach as quickly as possible. This tool automates the audit process, allowing for rapid detection of file-level changes that would take a human developer hours to find manually.

### 🛠️ Software Supply Chain Security
This project explores how developers can verify that their build environment remains "clean." By baseline-testing a project directory before a deployment, we ensure that no malicious artifacts or "extra" files have been injected into the software lifecycle.
