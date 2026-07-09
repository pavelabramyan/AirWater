// Copy to config.js and fill in. Prefer webhookUrl — never put bot tokens in public JS for production.
const AWC_CONFIG = {
    // Preferred: Formspree / Make.com / n8n / Cloudflare Worker webhook that forwards to Telegram/email
    webhookUrl: '',

    // Optional public contacts shown in footer (leave empty to hide)
    contactEmail: '',
    contactTelegram: '', // e.g. https://t.me/username
    contactPhone: '',    // e.g. +62...

    // Optional analytics (Plausible domain OR GA4 measurement id)
    plausibleDomain: '',
    gaMeasurementId: '' // e.g. G-XXXXXXXX
};
