Remove-Item -Path journal -Recurse -Force
Remove-Item -Path link -Recurse -Force
Remove-Item -Path mermaid -Recurse -Force
Remove-Item -Path minutes -Recurse -Force
Remove-Item -Path note -Recurse -Force
Remove-Item -Path reference -Recurse -Force
Remove-Item -Path templates -Recurse -Force
Remove-Item -Path todo -Recurse -Force
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\journal" -Destination ".\journal" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\link" -Destination ".\link" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\mermaid" -Destination ".\mermaid" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\minutes" -Destination ".\minutes" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\note" -Destination ".\note" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\reference" -Destination ".\reference" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\templates" -Destination ".\templates" -recurse
Copy-Item -Path "C:\Users\Mats Wiklander\Downloads\zettelkasten-backup\todo" -Destination ".\todo" -recurse
