# 🔧 Troubleshooting Guide

## 🎯 **Quick Problem Resolution**

This guide helps you diagnose and resolve common issues with the Enhanced CursorRules Architect. Most problems can be resolved quickly with the right diagnosis.

---

## 🚨 **Emergency Quick Fixes**

### **System Won't Start**
```bash
# 1. Check dependencies
python -c "import numpy, jsonschema; print('✅ Dependencies OK')"

# 2. Check configuration
python -c "
from core.context_engineering.integration_manager import IntegrationConfig
config = IntegrationConfig()
print('✅ Configuration OK')
"

# 3. Run in fallback mode
python main_enhanced.py /path/to/project --disable-context-engineering
```

### **Analysis Fails Immediately**
```bash
# Check system status
python -c "
from main_enhanced import EnhancedCursorRulesProjectAnalyzer
analyzer = EnhancedCursorRulesProjectAnalyzer()
print(analyzer.get_system_status())
"

# Run with verbose logging
export CONTEXT_ENGINEERING_LOG_LEVEL=DEBUG
python main_enhanced.py /path/to/project
```

### **Out of Memory Errors**
```bash
# Reduce memory usage immediately
export CONTEXT_ENGINEERING_MEMORY_LIMIT="25"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="2000"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="100000"
python main_enhanced.py /path/to/project
```

---

## 🔍 **Diagnostic Tools**

### **System Health Check**
```python
from main_enhanced import EnhancedCursorRulesProjectAnalyzer
from core.context_engineering.integration_manager import validate_context_engineering_dependencies

def run_full_diagnostic():
    print("🔍 Enhanced CursorRules Diagnostic Report")
    print("=" * 50)
    
    # 1. Check dependencies
    print("\n📦 Dependency Check:")
    deps_ok, issues = validate_context_engineering_dependencies()
    if deps_ok:
        print("✅ All dependencies satisfied")
    else:
        print(f"❌ Dependency issues found:")
        for issue in issues:
            print(f"   - {issue}")
    
    # 2. Check system status
    print("\n🔧 System Status:")
    try:
        analyzer = EnhancedCursorRulesProjectAnalyzer()
        status = analyzer.get_system_status()
        
        print(f"Context Engineering Available: {status['context_engineering_available']}")
        print(f"Context Engineering Enabled: {status['context_engineering_enabled']}")
        
        if 'enhancement_metrics' in status:
            metrics = status['enhancement_metrics']
            print(f"Enhancement Attempts: {metrics.get('context_engineering_attempts', 0)}")
            print(f"Enhancement Successes: {metrics.get('context_engineering_successes', 0)}")
            print(f"Fallback Uses: {metrics.get('fallback_uses', 0)}")
        
    except Exception as e:
        print(f"❌ System status check failed: {e}")
    
    # 3. Check configuration
    print("\n⚙️ Configuration Check:")
    try:
        from core.context_engineering.integration_manager import IntegrationConfig
        config = IntegrationConfig()
        print("✅ Configuration validation passed")
        print(f"Optimization Mode: {config.optimization_mode}")
        print(f"Field Capacity: {config.field_capacity}")
        print(f"Error Tolerance: {config.error_tolerance_level}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")

# Run the diagnostic
run_full_diagnostic()
```

### **Memory Usage Diagnostic**
```python
import psutil
import os

def check_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"Current Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"Virtual Memory: {memory_info.vms / 1024 / 1024:.2f} MB")
    
    # System memory
    system_memory = psutil.virtual_memory()
    print(f"System Memory Available: {system_memory.available / 1024 / 1024:.2f} MB")
    print(f"System Memory Usage: {system_memory.percent}%")
    
    return memory_info.rss / 1024 / 1024  # Return current usage in MB

current_usage = check_memory_usage()
if current_usage > 500:  # More than 500MB
    print("⚠️ High memory usage detected - consider reducing configuration")
```

### **Performance Diagnostic**
```python
import time
import asyncio
from main_enhanced import EnhancedCursorRulesProjectAnalyzer

async def performance_test():
    print("🚀 Performance Test")
    print("-" * 30)
    
    start_time = time.time()
    
    try:
        analyzer = EnhancedCursorRulesProjectAnalyzer(enable_context_engineering=True)
        
        # Test with current directory (small test)
        result = await analyzer.run_analysis(".")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Analysis completed in {duration:.2f} seconds")
        
        # Check enhancement level
        enhancement_meta = result.get("_global_enhancement_metadata", {})
        enhancement_level = enhancement_meta.get("enhancement_level", "unknown")
        print(f"Enhancement Level: {enhancement_level}")
        
        if duration > 300:  # More than 5 minutes
            print("⚠️ Analysis took longer than expected")
            print("Consider using efficiency mode or reducing field capacity")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

# Run performance test
asyncio.run(performance_test())
```

---

## ❗ **Common Issues and Solutions**

### **Issue: "No module named 'numpy'"**

#### **Symptoms:**
- Error on startup: `ImportError: No module named 'numpy'`
- Context engineering shows as unavailable
- System falls back to original mode

#### **Solutions:**
```bash
# Solution 1: Install missing dependencies
pip install numpy jsonschema

# Solution 2: Use virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install numpy jsonschema

# Solution 3: Continue without context engineering
export CONTEXT_ENGINEERING_ENABLED="false"
python main_enhanced.py /path/to/project
```

#### **Verification:**
```python
try:
    import numpy as np
    import jsonschema
    print("✅ Dependencies installed successfully")
    print(f"NumPy version: {np.__version__}")
except ImportError as e:
    print(f"❌ Still missing: {e}")
```

---

### **Issue: Analysis Hangs or Takes Forever**

#### **Symptoms:**
- Analysis starts but never completes
- High CPU usage for extended periods
- No progress indicators

#### **Diagnosis:**
```python
# Check if it's actually hung or just slow
import time
from main_enhanced import EnhancedCursorRulesProjectAnalyzer

def test_with_timeout():
    analyzer = EnhancedCursorRulesProjectAnalyzer()
    status = analyzer.get_system_status()
    
    if status.get('context_engineering_enabled'):
        print("Context engineering is enabled - this may take longer")
        print("Current configuration likely needs tuning")
    
    # Check for large project
    import os
    file_count = sum(len(files) for _, _, files in os.walk("."))
    print(f"Project has {file_count} files")
    
    if file_count > 10000:
        print("⚠️ Large project detected - consider using efficiency mode")

test_with_timeout()
```

#### **Solutions:**
```bash
# Solution 1: Use efficiency mode
export CONTEXT_ENGINEERING_MODE="efficiency"
export CONTEXT_ENGINEERING_TIMEOUT="120"  # 2 minutes
python main_enhanced.py /path/to/project

# Solution 2: Reduce resource usage
export CONTEXT_ENGINEERING_FIELD_CAPACITY="2000"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="100000"
python main_enhanced.py /path/to/project

# Solution 3: Disable heavy components
export CONTEXT_ENGINEERING_FIELD_DYNAMICS="false"
export CONTEXT_ENGINEERING_COGNITIVE_TOOLS="false"
python main_enhanced.py /path/to/project

# Solution 4: Use original mode for comparison
python main_enhanced.py /path/to/project --disable-context-engineering
```

---

### **Issue: Memory Usage Too High**

#### **Symptoms:**
- System runs out of memory
- `MemoryError` exceptions
- System becomes unresponsive

#### **Diagnosis:**
```python
def diagnose_memory_issue():
    import psutil
    
    # Check system memory
    memory = psutil.virtual_memory()
    print(f"Total RAM: {memory.total / 1024**3:.2f} GB")
    print(f"Available: {memory.available / 1024**3:.2f} GB")
    print(f"Used: {memory.percent}%")
    
    if memory.available < 2 * 1024**3:  # Less than 2GB available
        print("⚠️ Low system memory - need to reduce configuration")
        return "low_memory"
    elif memory.percent > 80:
        print("⚠️ High memory usage - monitor closely")
        return "high_usage"
    else:
        print("✅ Memory usage looks normal")
        return "normal"

memory_status = diagnose_memory_issue()
```

#### **Solutions:**
```bash
# For systems with <4GB RAM
export CONTEXT_ENGINEERING_MEMORY_LIMIT="25"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="1500"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="50000"

# For systems with <8GB RAM
export CONTEXT_ENGINEERING_MEMORY_LIMIT="50"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="3000"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="200000"

# Minimal configuration
export CONTEXT_ENGINEERING_FIELD_DYNAMICS="false"
export CONTEXT_ENGINEERING_ATOMIC_PROMPTING="true"
export CONTEXT_ENGINEERING_COGNITIVE_TOOLS="false"
```

---

### **Issue: Context Engineering Not Working**

#### **Symptoms:**
- All analyses show `enhanced: false`
- No `_context_engineering` sections in output
- System appears to run in original mode

#### **Diagnosis:**
```python
def diagnose_context_engineering():
    from main_enhanced import EnhancedCursorRulesProjectAnalyzer
    from core.context_engineering.integration_manager import validate_context_engineering_dependencies
    
    print("🔍 Context Engineering Diagnosis")
    
    # 1. Check dependencies
    deps_ok, issues = validate_context_engineering_dependencies()
    if not deps_ok:
        print("❌ Dependencies missing:")
        for issue in issues:
            print(f"   - {issue}")
        return "dependencies"
    
    # 2. Check initialization
    try:
        analyzer = EnhancedCursorRulesProjectAnalyzer(enable_context_engineering=True)
        status = analyzer.get_system_status()
        
        if not status['context_engineering_enabled']:
            print("❌ Context engineering disabled")
            return "disabled"
        
        if not status['context_engineering_healthy']:
            print("❌ Context engineering unhealthy")
            return "unhealthy"
        
        print("✅ Context engineering should be working")
        return "working"
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return "initialization_failed"

issue = diagnose_context_engineering()
```

#### **Solutions:**
```python
# Solution based on diagnosis
if issue == "dependencies":
    print("Install: pip install numpy jsonschema")
elif issue == "disabled":
    print("Enable: export CONTEXT_ENGINEERING_ENABLED=true")
elif issue == "unhealthy":
    print("Check logs and restart system")
elif issue == "initialization_failed":
    print("Check configuration and try fallback mode")
```

---

### **Issue: Inconsistent Results**

#### **Symptoms:**
- Different results on repeated runs
- Analysis quality varies significantly
- Enhancement level changes unexpectedly

#### **Diagnosis:**
```python
async def test_consistency():
    from main_enhanced import EnhancedCursorRulesProjectAnalyzer
    
    results = []
    
    for i in range(3):
        print(f"Run {i+1}...")
        analyzer = EnhancedCursorRulesProjectAnalyzer()
        result = await analyzer.run_analysis(".")
        
        enhancement_meta = result.get("_global_enhancement_metadata", {})
        enhancement_level = enhancement_meta.get("enhancement_level", "unknown")
        enhanced_phases = len(enhancement_meta.get("enhanced_phases", []))
        
        results.append({
            "enhancement_level": enhancement_level,
            "enhanced_phases": enhanced_phases,
            "has_error": "error" in result
        })
    
    # Check consistency
    levels = [r["enhancement_level"] for r in results]
    if len(set(levels)) > 1:
        print("⚠️ Inconsistent enhancement levels:", levels)
    else:
        print("✅ Consistent enhancement levels")
    
    return results

# Run consistency test
results = asyncio.run(test_consistency())
```

#### **Solutions:**
```bash
# Solution 1: Set strict error tolerance
export CONTEXT_ENGINEERING_ERROR_TOLERANCE="strict"

# Solution 2: Disable adaptive behavior
export CONTEXT_ENGINEERING_ENABLE_FALLBACK="false"

# Solution 3: Use fixed configuration
export CONTEXT_ENGINEERING_MODE="balanced"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="8000"

# Solution 4: Check for resource contention
# Make sure system has consistent available resources
```

---

### **Issue: Configuration Not Taking Effect**

#### **Symptoms:**
- Environment variables ignored
- Configuration file changes have no effect
- System uses default values

#### **Diagnosis:**
```python
def check_configuration_loading():
    import os
    from core.context_engineering.integration_manager import IntegrationConfig
    
    print("🔍 Configuration Loading Check")
    
    # Check environment variables
    env_vars = {
        'CONTEXT_ENGINEERING_MODE': os.getenv('CONTEXT_ENGINEERING_MODE'),
        'CONTEXT_ENGINEERING_MEMORY_LIMIT': os.getenv('CONTEXT_ENGINEERING_MEMORY_LIMIT'),
        'CONTEXT_ENGINEERING_FIELD_CAPACITY': os.getenv('CONTEXT_ENGINEERING_FIELD_CAPACITY'),
    }
    
    print("Environment Variables:")
    for key, value in env_vars.items():
        print(f"  {key}: {value}")
    
    # Check configuration object
    try:
        config = IntegrationConfig()
        print(f"\nActual Configuration:")
        print(f"  optimization_mode: {config.optimization_mode}")
        print(f"  field_capacity: {config.field_capacity}")
        print(f"  error_tolerance_level: {config.error_tolerance_level}")
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")

check_configuration_loading()
```

#### **Solutions:**
```bash
# Solution 1: Check environment variable format
export CONTEXT_ENGINEERING_MODE="balanced"  # Use quotes
export CONTEXT_ENGINEERING_FIELD_CAPACITY="8000"  # Numbers as strings

# Solution 2: Use programmatic configuration
python -c "
from core.context_engineering.integration_manager import IntegrationConfig
config = IntegrationConfig(
    optimization_mode='efficiency',
    field_capacity=4000
)
print('Config created:', config.optimization_mode)
"

# Solution 3: Check configuration file path
ls -la config/context_engineering.json

# Solution 4: Override with command line
python main_enhanced.py /path/to/project --optimization-mode efficiency
```

---

## 🔧 **Advanced Troubleshooting**

### **Debug Mode Activation**
```bash
# Enable comprehensive debugging
export CONTEXT_ENGINEERING_LOG_LEVEL="DEBUG"
export PYTHONPATH=/path/to/enhanced-cursorrules

# Run with detailed logging
python main_enhanced.py /path/to/project > analysis.log 2>&1

# Check the log file
tail -f analysis.log
```

### **Component-Specific Debugging**

#### **Field Dynamics Issues**
```python
def debug_field_dynamics():
    from core.context_engineering.field_dynamics import FieldDynamics, FieldType
    
    try:
        # Test field creation
        field_dynamics = FieldDynamics(max_fields=5, memory_limit_mb=10)
        
        # Test field creation
        success = field_dynamics.create_field("test", FieldType.DISCOVERY, {"test": "data"})
        print(f"Field creation: {'✅' if success else '❌'}")
        
        # Test health check
        health = field_dynamics.get_system_health()
        print(f"Health status: {health['health_status']}")
        print(f"Memory usage: {health['memory_usage_mb']:.2f} MB")
        
    except Exception as e:
        print(f"❌ Field dynamics error: {e}")
        import traceback
        traceback.print_exc()

debug_field_dynamics()
```

#### **Integration Manager Issues**
```python
def debug_integration_manager():
    from core.context_engineering.integration_manager import (
        ContextEngineeringIntegrationManager, 
        IntegrationConfig
    )
    
    try:
        config = IntegrationConfig()
        manager = ContextEngineeringIntegrationManager(config)
        
        # Test enhancement
        test_data = {"test": "data"}
        result = manager.enhance_phase("test_phase", test_data, None)
        
        if result.get("status") in ["error_fallback", "timeout_fallback"]:
            print(f"❌ Enhancement failed: {result.get('error_message')}")
        else:
            print("✅ Integration manager working")
            
    except Exception as e:
        print(f"❌ Integration manager error: {e}")
        import traceback
        traceback.print_exc()

debug_integration_manager()
```

### **Performance Profiling**
```python
import cProfile
import pstats
import asyncio
from main_enhanced import EnhancedCursorRulesProjectAnalyzer

async def profile_analysis():
    analyzer = EnhancedCursorRulesProjectAnalyzer()
    await analyzer.run_analysis(".")

# Run with profiling
cProfile.run('asyncio.run(profile_analysis())', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(20)
```

---

## 📊 **Monitoring and Alerts**

### **Basic Monitoring Script**
```python
import time
import json
from main_enhanced import EnhancedCursorRulesProjectAnalyzer

def monitor_system():
    analyzer = EnhancedCursorRulesProjectAnalyzer()
    
    while True:
        try:
            status = analyzer.get_system_status()
            
            # Check key metrics
            alerts = []
            
            if not status.get('context_engineering_enabled'):
                alerts.append("Context engineering disabled")
            
            metrics = status.get('enhancement_metrics', {})
            success_rate = 0
            if metrics.get('context_engineering_attempts', 0) > 0:
                success_rate = metrics['context_engineering_successes'] / metrics['context_engineering_attempts']
            
            if success_rate < 0.8:
                alerts.append(f"Low success rate: {success_rate:.2%}")
            
            # Log status
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            log_entry = {
                'timestamp': timestamp,
                'status': status,
                'alerts': alerts
            }
            
            with open('system_monitor.log', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            if alerts:
                print(f"🚨 {timestamp} - Alerts: {', '.join(alerts)}")
            else:
                print(f"✅ {timestamp} - System healthy")
            
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
        
        time.sleep(60)  # Check every minute

# Run monitoring (comment out for actual use)
# monitor_system()
```

---

## 🚑 **Emergency Recovery Procedures**

### **Complete System Reset**
```bash
# 1. Stop all processes
pkill -f "python.*main_enhanced"

# 2. Clear environment
unset CONTEXT_ENGINEERING_MODE
unset CONTEXT_ENGINEERING_MEMORY_LIMIT
unset CONTEXT_ENGINEERING_FIELD_CAPACITY

# 3. Reset to defaults and test
python -c "
from main_enhanced import EnhancedCursorRulesProjectAnalyzer
analyzer = EnhancedCursorRulesProjectAnalyzer(enable_context_engineering=False)
print('✅ Basic system working')
"

# 4. Gradually re-enable features
export CONTEXT_ENGINEERING_ENABLED="true"
export CONTEXT_ENGINEERING_MODE="efficiency"
python main_enhanced.py /path/to/small/project
```

### **Fallback to Original Mode**
```bash
# Ensure original functionality always works
python main_enhanced.py /path/to/project --disable-context-engineering

# If that fails, use the original main.py
python main.py /path/to/project
```

---

## 📞 **Getting Help**

### **Log Collection for Support**
```bash
# Collect comprehensive diagnostic information
python -c "
import sys
import platform
from main_enhanced import EnhancedCursorRulesProjectAnalyzer
from core.context_engineering.integration_manager import validate_context_engineering_dependencies

print('System Information:')
print(f'Python Version: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.architecture()}')

print('\nDependency Check:')
deps_ok, issues = validate_context_engineering_dependencies()
print(f'Dependencies OK: {deps_ok}')
for issue in issues:
    print(f'  - {issue}')

print('\nSystem Status:')
try:
    analyzer = EnhancedCursorRulesProjectAnalyzer()
    status = analyzer.get_system_status()
    for key, value in status.items():
        print(f'{key}: {value}')
except Exception as e:
    print(f'Error: {e}')
" > diagnostic_report.txt

# Send diagnostic_report.txt with your support request
```

### **Community Resources**
- 📖 [Documentation](../README.md)
- 💬 [GitHub Discussions](https://github.com/your-org/enhanced-cursorrules/discussions)
- 🐛 [Issue Tracker](https://github.com/your-org/enhanced-cursorrules/issues)
- 📧 [Email Support](mailto:support@your-org.com)

---

**🎉 Most issues can be resolved quickly with the right approach!**

Remember: The system is designed to be resilient. When in doubt, try the fallback mode first, then gradually re-enable features to isolate the problem.

*The Enhanced CursorRules Architect is built to never fail completely - there's always a path to getting results!* 🚀