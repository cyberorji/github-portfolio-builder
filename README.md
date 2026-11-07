# GitHub Portfolio Builder

GitHub kullanıcı adından hızlıca statik portföy sitesi üreten, Python standart kütüphanesiyle yazılmış çapraz platform CLI. Harici paket gerektirmez; Linux, Windows ve Termux üzerinde çalışır.

## Özellikler

- GitHub API'den genel profil ve depo bilgilerini alma
- Tek bir HTML dosyası üretme
- GitHub token olmadan public profil kullanımı
- Token ile rate-limit artırma desteği
- Türkçe ve İngilizce arayüz

## Kurulum ve kullanım

### Linux

```bash
git clone https://github.com/cyberorji/github-portfolio-builder.git
cd github-portfolio-builder
python3 portfolio.py --user cyberorji --out portfolio.html
python3 -m http.server 8000
```

### Windows PowerShell

```powershell
git clone https://github.com/cyberorji/github-portfolio-builder.git
Set-Location github-portfolio-builder
py portfolio.py --user cyberorji --out portfolio.html
py -m http.server 8000
```

### Termux

```bash
pkg update
pkg install python git
git clone https://github.com/cyberorji/github-portfolio-builder.git
cd github-portfolio-builder
python portfolio.py --user cyberorji --out portfolio.html
python -m http.server 8000
```

İsterseniz token vererek rate-limit'i artırabilirsiniz:

```bash
python portfolio.py --user octocat --token GH_TOKEN --lang en
```

## Lisans

MIT
