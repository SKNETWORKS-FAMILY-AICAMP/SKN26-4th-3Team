const HANGUL_BASE = 0xac00;
const HANGUL_END = 0xd7a3;
const JONGSUNG_COUNT = 28;

const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const getLastHangulSyllable = (value: string) => {
  const chars = Array.from(value.trim()).reverse();
  return chars.find((char) => {
    const code = char.charCodeAt(0);
    return code >= HANGUL_BASE && code <= HANGUL_END;
  });
};

export const hasFinalConsonant = (value: string) => {
  const syllable = getLastHangulSyllable(value);
  if (!syllable) return false;

  return (syllable.charCodeAt(0) - HANGUL_BASE) % JONGSUNG_COUNT !== 0;
};

export const subjectParticle = (value: string) => (hasFinalConsonant(value) ? "은" : "는");

export const normalizeSubjectParticle = (text: string, subject: string) => {
  if (!subject.trim()) return text;

  const particle = subjectParticle(subject);
  const subjectPattern = escapeRegExp(subject.trim()).replace(/\s+/g, "\\s+");
  const pattern = new RegExp(`(${subjectPattern})\\s*(은|는)`, "g");

  return text.replace(pattern, `$1${particle}`);
};
