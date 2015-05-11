#!/bin/sh

DOMAIN='brasil.gov.portal'

# Assume I18NDUDE is installed with buildout
# and this script is run under src/ folder with three nested namespaces in the package name
I18NDUDE=../../../../bin/i18ndude

if test ! -e $I18NDUDE; then
        I18NDUDE=i18ndude
        if test ! -e $I18NDUDE; then
                echo "No i18ndude was found in buildout or in your \$PATH."
                exit 1
        fi
fi

$I18NDUDE rebuild-pot --pot ./locales/${DOMAIN}.pot --merge ./locales/manual.pot --create ${DOMAIN} .  || exit 1
$I18NDUDE sync --pot ./locales/${DOMAIN}.pot ./locales/*/LC_MESSAGES/${DOMAIN}.po

$I18NDUDE rebuild-pot --pot ./locales/plone.pot --create plone ./profiles/default  || exit 1
$I18NDUDE sync --pot ./locales/plone.pot ./locales/*/LC_MESSAGES/plone.po

WARNINGS=`find . -name "*pt" | xargs $I18NDUDE find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs $I18NDUDE find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs $I18NDUDE find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./locales/rebuild_i18n.log
touch ./locales/rebuild_i18n.log

find ./ -name "*pt" | xargs $I18NDUDE find-untranslated > ./locales/rebuild_i18n.log
