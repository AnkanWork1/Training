const { spawn } = require('child_process');
const fs = require('fs/promises');
const path = require('path');

async function runProgramAndLogMetrics(programPath, logFilePath) {
    const logDir = path.dirname(logFilePath);
    
    // Ensure the log directory exists
    try {
        await fs.mkdir(logDir, { recursive: true });
    } catch (err) {
        console.error(`Failed to create log directory ${logDir}: ${err.message}`);
        process.exit(1);
    }

    // Capture starting metrics
    const startTime = Date.now();
    const startCpuUsage = process.cpuUsage();
    const startResourceUsage = process.resourceUsage();

    console.log(`\n--- Starting Target Program: ${programPath} ---`);
    console.log("Output of target program will appear below:");

    // Spawn the target program as a child process
    const child = spawn('node', [programPath], { stdio: 'inherit' });

    // Wait for the child process to close
    await new Promise((resolve, reject) => {
        child.on('close', (code) => {
            if (code !== 0) {//code has been terminated
                console.error(`\nTarget program exited with code ${code}`);
            }
            resolve();
        });
        child.on('error', (err) => {
            reject(err);
        });
    });

    console.log("\n--- Target Program Finished ---");

    // Capture ending metrics
    const endTime = Date.now();
    const endCpuUsage = process.cpuUsage();
    const endResourceUsage = process.resourceUsage();
    const runtimeMs = endTime - startTime;

    // Calculate the difference in CPU usage (microsecond values)
    const cpuUsageDiff = {
        user: endCpuUsage.user - startCpuUsage.user,
        system: endCpuUsage.system - startCpuUsage.system
    };

    // Prepare data for JSON log file
    const metrics = {
        timestamp: new Date().toISOString(),
        program: programPath,
        runtime_ms: runtimeMs,
        cpu_usage_mcros: cpuUsageDiff,
        resource_usage: endResourceUsage,
        notes: "CPU usage values are total microseconds consumed by the metric script AND the child process during execution time."
    };

    // Store the metrics in the specified JSON file
    try {
        await fs.writeFile(logFilePath, JSON.stringify(metrics, null, 2));
        console.log(`✅ Metrics successfully stored in: ${logFilePath}`);
    } catch (err) {
        console.error(`Error writing metrics to file: ${err.message}`);
    }
}

// Define the target program path and the required log file path
const targetProgram = './sysnfo.js'; 
const logFile = './logs/day1-sysmetrics.json'; 


runProgramAndLogMetrics(targetProgram, logFile);
