import Vue from 'vue';
import VueI18n from 'vue-i18n';
import { fallbackLocale } from '@/app.config';
import messages from '@intlify/unplugin-vue-i18n/messages';
import { createI18n } from 'vue-i18n-bridge';

function checkDefaultLanguage() {
  let matched = null;
  let languages = Object.getOwnPropertyNames(messages);
  languages.forEach(lang => {
    if (lang === navigator.language) {
      matched = lang;
    }
  });
  if (!matched) {
    languages.forEach(lang => {
      let languagePartials = navigator.language.split('-')[0];
      if (lang === languagePartials) {
        matched = lang;
      }
    });
  }
  if (!matched) {
    languages.forEach(lang => {
      let languagePartials = navigator.language.split('-')[0];
      if (lang.split('-')[0] === languagePartials) {
        matched = lang;
      }
    });
  }
  return matched;
}

export const selectedLocale = checkDefaultLanguage() || fallbackLocale;

export const languages = Object.getOwnPropertyNames(messages);

Vue.use(VueI18n, { bridge: true });

const i18n = createI18n(
  {
    locale: selectedLocale,
    fallbackLocale: fallbackLocale,
    messages,
    silentTranslationWarn: false,
  },
  VueI18n
);

Vue.use(i18n);

export default i18n;
