# Dépendances

- Python 3.7+, sur les linux modernes, une version fonctionnelle est déjà installée. Sur Windows, vous pouvez l'installer via le [MicrosoftStore](https://www.microsoft.com/store/productId/9NJ46SX7X90P?ocid=pdpshare)
- Flask, à installer via la ligne de commande suivante : `python3.7 -m pip install flask`
- Intel® Quartus® [19.1](https://www.intel.com/content/www/us/en/software-kit/664527/intel-quartus-prime-lite-edition-design-software-version-19-1-for-windows.html) (non testé sur d'autres versions)
- Un navigateur web moderne (autre que Internet Explorer)

## Dépendances materielles

- Un FPGA, pour notre cas nous avons travaillé sur la carte [DE0-CV](https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&CategoryNo=163&No=921)
- Un câble USB <-> UART

## Dépendances optionelles

- Dans le cas où vous souhaitez héberger vous même ce MdBook, suivez la page d'installation de leur documentation [Documentation MdBook](https://rust-lang.github.io/mdBook/guide/installation.html)
- L'outil de versionnement [Git](https://git-scm.com/downloads), dans le cas où vous souhaitez cloner directement les sources.

# Installation

Vous retrouverez toutes les sources sur le repository [GitHub suivant](https://github.com/SimonHauguel/Generic-ANN).
Vous pouvez le cloner via : `git clone https://github.com/SimonHauguel/Generic-ANN.git`

Une fois installé, vous trouverez un fichier d'example `wmatrix` et un dossier `web`. Dans le dossier `web` se trouve, les fichiers sources python et les fichiers sources de ce MdBook.