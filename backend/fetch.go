package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "path/filepath"
)

func fetchCVEDetails(dependenciesFile string, outputDir string) {
    // Read the dependencies file
    data, err := ioutil.ReadFile(dependenciesFile)
    if err != nil {
        fmt.Printf("Failed to read dependencies file: %v\n", err)
        return
    }

    // Parse the dependencies JSON
    var dependencies map[string]string
    err = json.Unmarshal(data, &dependencies)
    if err != nil {
        fmt.Printf("Failed to parse dependencies file: %v\n", err)
        return
    }

    // Create output directory if it doesn't exist
    err = os.MkdirAll(outputDir, os.ModePerm)
    if err != nil {
        fmt.Printf("Failed to create output directory: %v\n", err)
        return
    }

    for pkg, version := range dependencies {
        if version != "" && version != "version not found" && version != "null" {
            url := fmt.Sprintf("https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=%s+%s", pkg, version)
            fmt.Printf("Fetching CVE details for %s %s from %s\n", pkg, version, url)

            resp, err := http.Get(url)
            if err != nil {
                fmt.Printf("Failed to fetch CVE details for %s %s: %v\n", pkg, version, err)
                continue
            }
            defer resp.Body.Close()

            if resp.StatusCode == http.StatusOK {
                // Save HTML content to a file
                filename := fmt.Sprintf("%s_%s.html", pkg, version)
                filepath := filepath.Join(outputDir, filename)
                body, err := ioutil.ReadAll(resp.Body)
                if err != nil {
                    fmt.Printf("Failed to read response body for %s %s: %v\n", pkg, version, err)
                    continue
                }

                err = ioutil.WriteFile(filepath, body, 0644)
                if err != nil {
                    fmt.Printf("Failed to save CVE details for %s %s to %s: %v\n", pkg, version, filepath, err)
                    continue
                }
                fmt.Printf("Saved CVE details for %s %s to %s\n", pkg, version, filepath)
            } else {
                fmt.Printf("Failed to fetch CVE details for %s %s. Status code: %d\n", pkg, version, resp.StatusCode)
            }
        }
    }
}

func main() {
    dependenciesFile := "dependencies.json"
    outputDir := "cve_pages"

    fetchCVEDetails(dependenciesFile, outputDir)
}

