Create a parallel file deduplication and compression engine that efficiently processes multiple files simultaneously.

Your system must implement the following components:

1. **Parallel File Processor**: Process files using at least 4 worker threads/processes
2. **Content-based Deduplication**: Identify duplicate files using SHA-256 hashes
3. **Compression Engine**: Compress unique files using gzip compression
4. **Metadata Storage**: Store deduplication statistics and file mappings
5. **Query Interface**: Provide commands to retrieve statistics and decompress files

## Implementation Requirements:

Create a Python script named `dedup_engine.py` that supports these commands:

### `python dedup_engine.py process <input_dir> <output_dir>`
- Process all files in input_dir using parallel workers (minimum 4 threads)
- Calculate SHA-256 hash for each file to identify duplicates
- Compress unique files and store in output_dir as `<hash>.gz`
- Save duplicate file mappings to avoid redundant compression
- Create a metadata file `dedup_stats.json` with processing statistics

### `python dedup_engine.py stats <output_dir>`
- Display deduplication statistics from the metadata file
- Show: total files processed, unique files, duplicates found, space saved, processing time

### `python dedup_engine.py extract <output_dir> <hash> <target_file>`
- Decompress and extract a file by its hash to target_file

## Test Data:
Use the provided sample files in `sample_files/` directory which contains:
- Multiple text files (some duplicates)
- Binary files (images)
- Files of varying sizes

## Performance Requirements:
- Must use parallel processing (concurrent.futures or multiprocessing)
- Processing should complete within 30 seconds for the test dataset
- Compression ratio should be logged in statistics
- Memory usage should be efficient (don't load entire large files at once)

## Output Format:
The `dedup_stats.json` should contain:
```json
{
  "total_files": <number>,
  "unique_files": <number>, 
  "duplicate_files": <number>,
  "total_size_bytes": <number>,
  "compressed_size_bytes": <number>,
  "space_saved_bytes": <number>,
  "compression_ratio": <float>,
  "processing_time_seconds": <float>,
  "file_mappings": {
    "original_path": "hash"
  }
}
```