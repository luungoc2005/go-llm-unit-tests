package ast_tool

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
)

func main() {
	fset := token.NewFileSet()
	inputFile := os.Args[1]
	f, err := parser.ParseFile(fset, inputFile, nil, 0)
	if err != nil {
		fmt.Println(err)
		return
	}
	ast.Inspect(f, func(n ast.Node) bool {
		funcCall, ok := n.(*ast.FuncDecl)
		if ok {
			fmt.Printf("%v:%v:%v\n", funcCall.Name.Name, fset.Position(funcCall.Pos()).Line, fset.Position(funcCall.End()).Line)
		}
		return true
	})
}
