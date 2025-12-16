

const os = require('os');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function getSystemInfoUbuntu() {
    console.log("Gathering Ubuntu system information...");

    // 1. Host Name
    console.log(`\nHostname: ${os.hostname()}`);

    // 2. Available Disk Space (using 'df -h' command)
    console.log("\nAvailable Disk Space:");
    try {
        // 'df -h /' checks the root partition
        const { stdout } = await execPromise('df -h /');
        console.log(stdout.trim()); // Prints the formatted output directly from 'df -h'
    } catch (err) {
        console.error(`Error running df: ${err.message}`);
    }

    // 3. Open Ports (Top 5) (using 'ss' is often preferred over 'netstat' on modern Ubuntu)
    console.log("\nOpen Ports (Top 5 Listening):");
    try {
        // ss -tuln = summary, tcp/udp, listening, no resolve
        const { stdout } = await execPromise('ss -tuln | head -n 6'); // 1 header + 5 ports
        console.log(stdout.trim());
    } catch (err) {
        console.error(`Error running ss (Do you have 'iproute2' installed?): ${err.message}`);
    }

    // 4. Default Gateway (using 'ip route' command)
    console.log("\nDefault Gateway:");
    try {
        const { stdout } = await execPromise('ip route | grep default');
        const match = stdout.match(/default via (\S+)/);
        if (match ) {
            console.log(`Gateway IP: ${match}`);
        } else {
            console.log("Could not parse default gateway from 'ip route' output.");
            console.log("Raw output:", stdout.trim());
        }
    } catch (err) {
        console.error(`Error running ip route: ${err.message}`);
    }

    // 5. Logged In Users Count
    console.log("\nLogged In Users Count:");
    try {
        const { stdout } = await execPromise('who | wc -l');
        console.log(stdout.trim());
    } catch (err) {
        console.error(`Error running who/wc -l: ${err.message}`);
    }
}

getSystemInfoUbuntu();

