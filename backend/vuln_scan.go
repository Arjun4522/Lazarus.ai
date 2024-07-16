package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
)

// Notebook represents the structure of a Jupyter notebook.
type Notebook struct {
	Cells []Cell `json:"cells"`
}

// Cell represents a single cell in a Jupyter notebook.
type Cell struct {
	CellType string   `json:"cell_type"`
	Source   []string `json:"source"`
}

func readNotebook(filename string) (*Notebook, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	bytes, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}

	var notebook Notebook
	err = json.Unmarshal(bytes, &notebook)
	if err != nil {
		return nil, err
	}

	return &notebook, nil
}

func scanVulns(notebook *Notebook) {
	PATTERNS:=`(?:eval\(|exec\(|system\(|shell_exec\(|passthru\(|assert\(|popen\(|pcntl_exec\(|proc_open\(|dl\(|include\(|require\(|require_once\(|mysql_query\(|mysqli_query\(|pdo->query\(|mysqli_prepare\(|exec\(|os\.system\(|subprocess\.call\(|pickle\.load\(|xml\.etree\.ElementTree\(|pickle\.loads\(|XMLHttpRequest\(|sqlite_query\(|open\(|java\.lang\.Runtime\.getRuntime\(\.exec\(|new Function\(|localStorage\.setItem\(|document\.write\(|window\.open\()`
	r := regexp.MustCompile(PATTERNS)
	var vulns int
	
	for cell_no, cell := range notebook.Cells {
		if cell.CellType == "code" {
			for line_no, line := range cell.Source {
				matches := r.FindAllString(line, -1)
				if len(matches)!=0 {
					vulns ++
					fmt.Println("[Cell:",cell_no,"Line:",line_no,"]:",line)
					fmt.Println("Cause:",matches)
				}
			}
		}
	}

	fmt.Println("\nFound:",vulns,"Vulnerabilities!")
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run vuln_scan.go <input.ipynb> <output.py>")
		return
	}

	inputFile := os.Args[1]

	notebook, err := readNotebook(inputFile)
	if err != nil {
		fmt.Printf("Failed to read notebook: %v\n", err)
		return
	}

	scanVulns(notebook)
}
