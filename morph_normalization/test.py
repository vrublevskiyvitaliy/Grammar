#!/usr/bin/env python 
"""
Test file for morphology module
"""

import Morphology
import sys

morph = Morphology.Morphology('morph')
print morph.normalize('sleep')
