#!/usr/bin/env node
const fs = require('fs');
const readline = require('readline');
const path = require('path');

// Promisified function to process a single file and return metrics/counts
function processFile(types,filePath, removeDuplicates = false) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        const startMem = process.memoryUsage().heapUsed;

        //if file not existing or mismatched file path it terminates here.
        if (!fs.existsSync(filePath)) {
            return reject(new Error(`File not found: ${filePath}`));
        }

        const rl = readline.createInterface({// rl containinf the data in the files
            input: fs.createReadStream(filePath),//read the file here
            crlfDelay: Infinity
        });

        let linesCount = 0;
        let wordsCount = 0;
        let charsCount = 0;
        const uniqueLines = new Set();// using a set to counter uniqueness 
        const lines = [];// to store the unique lines

        rl.on('line', (line) => {
            linesCount++;
            charsCount += line.length + 1; // +1 for the newline character
            wordsCount += line.trim().split(/\s+/).filter(word => word.length > 0).length;

            if (removeDuplicates) {
                if (!uniqueLines.has(line)) {
                    uniqueLines.add(line);
                    lines.push(line);
                }
            }
        });

        rl.on('close', async () => {
            const endTime = Date.now();
            const endMem = process.memoryUsage().heapUsed;
            const executionTimeMs = endTime - startTime;
            const memoryMB = (endMem - startMem) / 1024 / 1024;

            const results = {
                file: path.basename(filePath),
                executionTimeMs,
                memoryMB,
                counts: {}
            };

            if (types.has("lines")) {
                results.counts.lines = linesCount;
            }
            if (types.has("words")) {
                results.counts.words = wordsCount;
            }
            if (types.has("chars")) {
                results.counts.chars = charsCount;
            }


            // Bonus: Handle unique lines output
            if (removeDuplicates) {
                const outputDir = path.join(process.cwd(), 'output');
                if (!fs.existsSync(outputDir)) {
                    fs.mkdirSync(outputDir, { recursive: true });
                }
                const outputFileName = `unique-${path.basename(filePath)}`;
                const outputPath = path.join(outputDir, outputFileName);
                await fs.promises.writeFile(outputPath, lines.join('\n') + '\n');
                console.log(`\nBonus: Unique lines written to: ${outputPath}`);
            }

            resolve(results);
        });

        rl.on('error', reject);
    });
}



async function main() {
    const args = process.argv.slice(2);
    let removeDuplicatesFlag = false;
    const filesToProcess = new Map();

    function validateFile(file) {
        return file && !file.startsWith('--');
    }

    for (let i = 0; i < args.length; i++) {

        if (["--lines", "--words", "--chars"].includes(args[i])) {

            const next = path.normalize(args[i + 1]);

            if (!next || next.startsWith("--")) {
                console.error(`Missing filename after ${args[i]}`);
                continue;
            }

            const metric = args[i].slice(2); // "lines" | "words" | "chars"
            console.log('${next}');
            if (!filesToProcess.has(next)) {
                filesToProcess.set(next, new Set());
            }

            filesToProcess.get(next).add(metric);
            i++; 
        }
        else if (args[i] === "--unique") {
            removeDuplicatesFlag = true;
        }
    }


    // FIX — correctly check number of keys
    if (filesToProcess.size === 0) {
    console.log("Usage: ...");
    process.exit(1);
}


    console.log(`\nProcessing ${filesToProcess.size} file(s) in parallel...`);

    const processingPromises = [];
    for (const [file, types] of filesToProcess) {
        processingPromises.push(processFile(types, file, removeDuplicatesFlag));
    }


    try {
        const results = await Promise.all(processingPromises);

        console.log("\n--- Performance Report & Stats ---");

        const logsDir = path.join(process.cwd(), 'logs');
        if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir, { recursive: true });

        results.forEach(result => {
            console.log(JSON.stringify(result, null, 2));

            const timestamp = Date.now();
            const logFileName = `performance-${result.file}-${timestamp}.json`;

            const logPath = path.join(logsDir, logFileName);
            fs.writeFileSync(logPath, JSON.stringify(result, null, 2));
            console.log(`(Report saved to ${logPath})\n`);
        });

    } catch (error) {
        console.error(`\nAn error occurred during processing: ${error.message}`);
        process.exit(1);
    }
}
main();