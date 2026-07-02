"""
Simple lightweight matching engine for Lost <-> Found items.
Uses category equality + item-name token similarity (no external deps).
"""
import difflib


def name_similarity(a, b):
    """Return a 0-1 similarity ratio between two item titles."""
    return difflib.SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def find_matches_for_lost(lost_item, found_qs, threshold=0.45):
    matches = []
    for found in found_qs.filter(category=lost_item.category, status='active'):
        score = name_similarity(lost_item.title, found.title)
        if score >= threshold:
            matches.append((found, round(score * 100)))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def find_matches_for_found(found_item, lost_qs, threshold=0.45):
    matches = []
    for lost in lost_qs.filter(category=found_item.category, status='active'):
        score = name_similarity(found_item.title, lost.title)
        if score >= threshold:
            matches.append((lost, round(score * 100)))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches
