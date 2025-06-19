#!/bin/bash

rm -rf allure-results

echo "Lancement des tests CATEGORY..."
pytest tests/func/category/test_test_add_category.py \
       tests/func/category/test_test_add_category_form.py \
       tests/func/category/test_test_edit_category.py \
       tests/func/category/test_test_delete_category.py \
       --alluredir=allure-results

echo "Lancement des tests PRODUCT..."
pytest tests/func/product/test_test_add_product.py \
       tests/func/product/test_test_edit_product.py \
       tests/func/product/test_test_delete_product.py \
       --alluredir=allure-results

echo "Lancement des tests SHOPPING..."
pytest tests/func/shooping --alluredir=allure-results

echo "Tests terminés, résultats dans allure-results/"
allure serve allure-results