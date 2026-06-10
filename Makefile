.PHONY: install test lint clean build dist upload help

PYTHON := python3
PIP := pip3

help:
	@echo "ImpactForge - 智能代码变更影响分析引擎"
	@echo ""
	@echo "可用命令:"
	@echo "  make install    安装依赖"
	@echo "  make test       运行测试"
	@echo "  make lint       代码检查"
	@echo "  make clean      清理构建文件"
	@echo "  make build      构建分发包"
	@echo "  make dist       生成 wheel 和 sdist"
	@echo "  make run        运行示例"
	@echo "  make help       显示此帮助"

install:
	$(PIP) install -e .
	$(PIP) install pytest

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m py_compile impactforge/*.py
	@echo "语法检查通过"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf impactforge/__pycache__/
	rm -rf tests/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

build: clean
	$(PYTHON) -m build

dist: build
	@echo "分发包已生成在 dist/ 目录"

run:
	$(PYTHON) -m impactforge.cli --help
