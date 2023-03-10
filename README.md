# Labelit

[![Build](https://github.com/voicelab-org/labelit/actions/workflows/build-push.yaml/badge.svg)](https://github.com/voicelab-org/labelit/actions/workflows/build-push.yaml)
[![](https://img.shields.io/github/v/release/voicelab-org/labelit)](https://github.com/voicelab-org/labelit/releases)
[![Backend tests](https://github.com/voicelab-org/labelit/actions/workflows/backend-tests.yaml/badge.svg?branch=master)](https://github.com/voicelab-org/labelit/actions/workflows/backend-tests.yaml)
[![Documentation Status](https://readthedocs.org/projects/labelit/badge/?version=latest)](https://labelit.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Introduction

Labelit is an extensible web-based annotation tool currently supporting:

- Text and audio annotation (summative)
- Categorical, ordinal classification
- Transcription
- Named entity annotation (highlighting and labeling)
- Text edition (correction, punctuation, etc.)
- Audio region segmentation

The tool comes with utilities for distributing work across multiple annotators, monitoring progress and (where applicable) annotator agreement, Quality Assurance (QA) and managing datasets.

Multiple annotation tasks (e.g. classification + transcription) can be combined in a single project.

Labelit is designed for extensibility: new annotation tasks / schemas can be created by contributors, while retaining generic features.

## Documentation

We maintain a documentation:

<p align="center">
  <a href="https://labelit.readthedocs.io/en/latest/">📖 Read our documentation 📖</a>
</p>

## Demo

A demo version of LabelIt is hosted at [https://labelit.demo.batvoice.ai](https://labelit.demo.batvoice.ai)


| Account type | Username | Password |
|---|---|---|
| Annotator account | `demo@demo.com` | `dem0#nnotator` |
| QA account | `qa@qa.com` | `demo` |

## Maintainers / Sponsors

This project is activly maintained by :

<p align="center">
  <a href="https://www.batvoice.com/" target="_blank">
    <img src="documentation/docs/assets/logo_batvoice.png" alt="BatvoiceAI">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.levoicelab.org/" target="_blank">
    <img src="documentation/docs/assets/logo_le_voice_lab.png" alt="LeVoiceLab">
  </a>
</p>
