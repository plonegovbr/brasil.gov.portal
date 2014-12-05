#!/bin/sh

DOMAIN='brasil.gov.portal'

i18ndude rebuild-pot --pot ./locales/${DOMAIN}.pot --merge ./locales/manual.pot --create ${DOMAIN} .  || exit 1
i18ndude sync --pot ./locales/${DOMAIN}.pot ./locales/*/LC_MESSAGES/${DOMAIN}.po

i18ndude rebuild-pot --pot ./locales/plone.pot --create plone ./profiles/default  || exit 1
i18ndude sync --pot ./locales/plone.pot ./locales/*/LC_MESSAGES/plone.po

WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./locales/rebuild_i18n.log
touch ./locales/rebuild_i18n.log

find ./ -name "*pt" | xargs i18ndude find-untranslated > ./locales/rebuild_i18n.log