import Vue from "vue";
import VueI18n from "vue-i18n";
import { fallbackLocale } from "@/app.config";

function loadLocaleMessages() {
  const locales = require.context(
    "./locales",
    true,
    /[A-Za-z0-9-_,\s]+\.json$/i
  );
  const messages = {};
  locales.keys().forEach((key) => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i);
    if (matched && matched.length > 1) {
      const locale = matched[1];
      messages[locale] = locales(key);
    }
  });
  return messages;
}

function checkDefaultLanguage() {
  let matched = null;
  let languages = Object.getOwnPropertyNames(loadLocaleMessages());
  languages.forEach((lang) => {
    if (lang === navigator.language) {
      matched = lang;
    }
  });
  if (!matched) {
    languages.forEach((lang) => {
      let languagePartials = navigator.language.split("-")[0];
      if (lang === languagePartials) {
        matched = lang;
      }
    });
  }
  if (!matched) {
    languages.forEach((lang) => {
      let languagePartials = navigator.language.split("-")[0];
      if (lang.split("-")[0] === languagePartials) {
        matched = lang;
      }
    });
  }
  return matched;
}

export const selectedLocale = checkDefaultLanguage() || fallbackLocale;

export const languages = Object.getOwnPropertyNames(loadLocaleMessages());

Vue.use(VueI18n);

export default new VueI18n({
  locale: selectedLocale,
  fallbackLocale: fallbackLocale,
  messages: loadLocaleMessages(),
  silentTranslationWarn: false,
});
