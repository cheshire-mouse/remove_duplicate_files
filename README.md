# remove_duplicate_files
Generates bash script to delete duplicate files from fdupes output 

    options:
      -h, --help            show this help message and exit
      --file FILE, -f FILE  duplicates list (fdupes output)
      --directories DIRECTORIES, -d DIRECTORIES
            directories list in order of priority (file from the directory, 
            which is listed first, will be saved)
      --gen-directories, -n
            generate list of directories
      --debug               verbose logging

1. Run fdupes with default options and save output to file
2. Generate directories list (-n option) using fdupes output (-f)
3. Sort directories list in the order of priority (file from the directory,
   which is listed first, will be saved)
4. Generate bash script, using dupes output (-f) and directories list (-d)
