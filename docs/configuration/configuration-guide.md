# ⚙️ Configuration Guide

## 🎯 **Complete Configuration Reference**

This guide covers all configuration options for the Enhanced CursorRules Architect with Context Engineering. The system is designed to work optimally out-of-the-box, but provides extensive customization for specific needs.

---

## 📋 **Configuration Hierarchy**

The system loads configuration in this order (later sources override earlier ones):

1. **Default Values** (built into the code)
2. **Environment Variables** 
3. **Configuration Files**
4. **Command Line Arguments**
5. **Programmatic Settings**

---

## 🔧 **Core Configuration Options**

### **Integration Configuration**

The main configuration class that controls all context engineering features:

```python
from core.context_engineering.integration_manager import IntegrationConfig

config = IntegrationConfig(
    # Feature toggles
    enable_atomic_prompting=True,
    enable_field_dynamics=True, 
    enable_cognitive_tools=True,
    enable_pattern_synthesis=True,
    
    # Performance settings
    optimization_mode="balanced",      # "efficiency", "depth", "balanced"
    field_capacity=8000,              # Maximum patterns per field
    max_context_size=500000,          # 500KB max context data
    max_processing_time=300,          # 5 minutes timeout
    
    # Reliability settings
    error_tolerance_level="moderate",  # "strict", "moderate", "permissive"
    enable_fallback=True,             # Enable automatic fallback
    token_efficiency_threshold=0.7    # Target efficiency (0.0-1.0)
)
```

### **Configuration Validation**

All configuration values are validated at startup:

```python
# Valid optimization modes
"efficiency"  # Prioritize speed and resource usage
"depth"      # Prioritize analysis quality and insights  
"balanced"   # Balance between efficiency and depth

# Valid error tolerance levels
"strict"     # Fail fast on any context engineering errors
"moderate"   # Try fallback, log errors, continue analysis
"permissive" # Continue with minimal logging even on errors

# Numeric ranges
field_capacity: 1000-50000          # Reasonable memory usage
token_efficiency_threshold: 0.0-1.0  # Percentage as decimal
max_context_size: 1000-10000000     # 1KB to 10MB
max_processing_time: 30-3600        # 30 seconds to 1 hour
```

---

## 🌍 **Environment Variables**

### **Core Settings**
```bash
# Enable/disable context engineering
export CONTEXT_ENGINEERING_ENABLED="true"

# Performance mode
export CONTEXT_ENGINEERING_MODE="balanced"  # efficiency, depth, balanced

# Resource limits
export CONTEXT_ENGINEERING_MEMORY_LIMIT="100"    # MB
export CONTEXT_ENGINEERING_FIELD_CAPACITY="8000"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="500000"  # bytes
export CONTEXT_ENGINEERING_TIMEOUT="300"             # seconds

# Error handling
export CONTEXT_ENGINEERING_ERROR_TOLERANCE="moderate"  # strict, moderate, permissive
export CONTEXT_ENGINEERING_ENABLE_FALLBACK="true"

# Token efficiency
export CONTEXT_ENGINEERING_TOKEN_THRESHOLD="0.7"
```

### **Feature Toggles**
```bash
# Individual feature control
export CONTEXT_ENGINEERING_ATOMIC_PROMPTING="true"
export CONTEXT_ENGINEERING_FIELD_DYNAMICS="true"
export CONTEXT_ENGINEERING_COGNITIVE_TOOLS="true"
export CONTEXT_ENGINEERING_PATTERN_SYNTHESIS="true"
```

### **Debugging and Monitoring**
```bash
# Logging levels
export CONTEXT_ENGINEERING_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR

# Performance monitoring
export CONTEXT_ENGINEERING_ENABLE_METRICS="true"
export CONTEXT_ENGINEERING_METRICS_INTERVAL="60"  # seconds

# Health checks
export CONTEXT_ENGINEERING_HEALTH_CHECK_INTERVAL="300"  # 5 minutes
```

---

## 📄 **Configuration Files**

### **Main Configuration File** (`config/context_engineering.json`)

```json
{
  "context_engineering": {
    "enabled": true,
    "features": {
      "atomic_prompting": {
        "enabled": true,
        "efficiency_threshold": 0.7,
        "optimization_templates": [
          "discovery",
          "analysis", 
          "synthesis",
          "reasoning"
        ]
      },
      "field_dynamics": {
        "enabled": true,
        "max_fields": 50,
        "memory_limit_mb": 100,
        "cleanup_interval": 300,
        "field_types": [
          "discovery",
          "reasoning", 
          "synthesis",
          "memory",
          "orchestration"
        ]
      },
      "cognitive_tools": {
        "enabled": true,
        "engines": {
          "understanding": true,
          "reasoning": true,
          "verification": true,
          "composition": true
        }
      }
    },
    "performance": {
      "optimization_mode": "balanced",
      "field_capacity": 8000,
      "max_context_size": 500000,
      "max_processing_time": 300,
      "token_efficiency_threshold": 0.7
    },
    "reliability": {
      "error_tolerance_level": "moderate",
      "enable_fallback": true,
      "max_retry_attempts": 3,
      "retry_delay": 1.0
    },
    "monitoring": {
      "enable_metrics": true,
      "metrics_interval": 60,
      "health_check_interval": 300,
      "log_level": "INFO"
    }
  }
}
```

### **Environment-Specific Configurations**

#### **Development Configuration** (`config/development.json`)
```json
{
  "context_engineering": {
    "enabled": true,
    "performance": {
      "optimization_mode": "depth",
      "max_processing_time": 600,
      "field_capacity": 12000
    },
    "reliability": {
      "error_tolerance_level": "strict"
    },
    "monitoring": {
      "log_level": "DEBUG",
      "enable_metrics": true
    }
  }
}
```

#### **Production Configuration** (`config/production.json`)
```json
{
  "context_engineering": {
    "enabled": true,
    "performance": {
      "optimization_mode": "efficiency",
      "max_processing_time": 180,
      "field_capacity": 6000,
      "max_context_size": 300000
    },
    "reliability": {
      "error_tolerance_level": "moderate",
      "enable_fallback": true,
      "max_retry_attempts": 2
    },
    "monitoring": {
      "log_level": "WARNING",
      "enable_metrics": true,
      "metrics_interval": 30
    }
  }
}
```

#### **Resource-Constrained Configuration** (`config/minimal.json`)
```json
{
  "context_engineering": {
    "enabled": true,
    "features": {
      "atomic_prompting": true,
      "field_dynamics": false,
      "cognitive_tools": false
    },
    "performance": {
      "optimization_mode": "efficiency",
      "field_capacity": 2000,
      "max_context_size": 100000,
      "max_processing_time": 120
    },
    "reliability": {
      "error_tolerance_level": "permissive"
    }
  }
}
```

---

## 🚀 **Performance Tuning**

### **Optimization Modes**

#### **Efficiency Mode**
```python
config = IntegrationConfig(
    optimization_mode="efficiency",
    field_capacity=4000,           # Smaller memory footprint
    max_context_size=200000,       # 200KB context limit
    max_processing_time=120,       # 2 minute timeout
    token_efficiency_threshold=0.8, # Higher efficiency required
    enable_field_dynamics=True,     # Keep core features
    enable_cognitive_tools=False    # Disable heavy processing
)
```

#### **Depth Mode**
```python
config = IntegrationConfig(
    optimization_mode="depth",
    field_capacity=12000,          # Larger memory for more patterns
    max_context_size=1000000,      # 1MB context limit
    max_processing_time=600,       # 10 minute timeout
    token_efficiency_threshold=0.6, # Accept lower efficiency for depth
    enable_field_dynamics=True,
    enable_cognitive_tools=True
)
```

#### **Balanced Mode** (Default)
```python
config = IntegrationConfig(
    optimization_mode="balanced",
    field_capacity=8000,
    max_context_size=500000,
    max_processing_time=300,
    token_efficiency_threshold=0.7
)
```

### **Memory Optimization**

#### **Low Memory Environment** (<4GB RAM)
```bash
export CONTEXT_ENGINEERING_MEMORY_LIMIT="50"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="3000"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="200000"
```

#### **High Memory Environment** (>16GB RAM)
```bash
export CONTEXT_ENGINEERING_MEMORY_LIMIT="200"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="15000"
export CONTEXT_ENGINEERING_MAX_CONTEXT_SIZE="1000000"
```

### **Processing Time Optimization**

#### **Fast Analysis** (CI/CD environments)
```bash
export CONTEXT_ENGINEERING_TIMEOUT="60"        # 1 minute
export CONTEXT_ENGINEERING_MODE="efficiency"
export CONTEXT_ENGINEERING_FIELD_DYNAMICS="false"  # Disable heavy processing
```

#### **Thorough Analysis** (overnight processing)
```bash
export CONTEXT_ENGINEERING_TIMEOUT="1800"      # 30 minutes
export CONTEXT_ENGINEERING_MODE="depth"
export CONTEXT_ENGINEERING_FIELD_CAPACITY="20000"
```

---

## 🛠️ **Advanced Configuration**

### **Custom Field Dynamics Configuration**

```python
from core.context_engineering.field_dynamics import FieldDynamics, FieldType

# Custom field dynamics with specific parameters
field_dynamics = FieldDynamics(
    max_fields=25,                    # Limit concurrent fields
    memory_limit_mb=75,              # Memory cap
    cleanup_interval=180,            # Clean up every 3 minutes
    field_config={
        FieldType.DISCOVERY: {
            "capacity": 4000,
            "decay_rate": 0.05,
            "activation_threshold": 0.7
        },
        FieldType.REASONING: {
            "capacity": 3000,
            "decay_rate": 0.08,
            "activation_threshold": 0.6
        }
    }
)
```

### **Custom Atomic Prompting Templates**

```python
from core.context_engineering.foundations import AtomicPromptingFoundation

atomic_foundation = AtomicPromptingFoundation(
    efficiency_threshold=0.8,
    custom_templates={
        "security_analysis": {
            "template": "Scan: {code_context} → security_vulnerabilities",
            "constraints": [
                "Focus on OWASP Top 10",
                "Identify authentication issues",
                "Flag insecure configurations"
            ],
            "max_tokens": 150
        },
        "performance_analysis": {
            "template": "Analyze: {code_context} → performance_bottlenecks",
            "constraints": [
                "Identify O(n²) algorithms",
                "Flag memory leaks",
                "Detect inefficient queries"
            ],
            "max_tokens": 200
        }
    }
)
```

### **Custom Cognitive Tools Configuration**

```python
from core.context_engineering.cognitive_tools import CognitiveToolkit

cognitive_toolkit = CognitiveToolkit(
    engines_config={
        "understanding": {
            "enabled": True,
            "depth_level": "comprehensive",  # basic, standard, comprehensive
            "context_window": 8000
        },
        "reasoning": {
            "enabled": True,
            "reasoning_chains": True,
            "cause_effect_analysis": True,
            "implications_analysis": True
        },
        "verification": {
            "enabled": True,
            "consistency_checks": True,
            "confidence_scoring": True,
            "evidence_validation": True
        }
    }
)
```

---

## 🔍 **Monitoring and Debugging Configuration**

### **Comprehensive Logging**

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('context_engineering.log'),
        logging.StreamHandler()
    ]
)

# Component-specific logging levels
logging.getLogger('core.context_engineering.integration_manager').setLevel(logging.DEBUG)
logging.getLogger('core.context_engineering.field_dynamics').setLevel(logging.INFO)
logging.getLogger('core.context_engineering.cognitive_tools').setLevel(logging.WARNING)
```

### **Performance Metrics Configuration**

```python
from core.context_engineering.integration_manager import ContextEngineeringIntegrationManager

# Enable comprehensive metrics
config = IntegrationConfig(
    enable_metrics=True,
    metrics_config={
        "track_token_efficiency": True,
        "track_processing_time": True,
        "track_memory_usage": True,
        "track_error_rates": True,
        "metrics_interval": 30,        # Update every 30 seconds
        "metrics_retention": 3600      # Keep 1 hour of metrics
    }
)
```

### **Health Check Configuration**

```python
config = IntegrationConfig(
    health_check_config={
        "enabled": True,
        "interval": 300,                    # Check every 5 minutes
        "field_health_threshold": 0.1,      # Field stability minimum
        "memory_usage_threshold": 0.9,      # Memory usage warning
        "error_rate_threshold": 0.1,        # Error rate warning
        "auto_cleanup": True,               # Automatic cleanup on issues
        "alert_on_degradation": True        # Alert when enhancement degrades
    }
)
```

---

## 🔐 **Security Configuration**

### **Data Sanitization**

```python
config = IntegrationConfig(
    security_config={
        "enable_input_sanitization": True,
        "sensitive_patterns": [
            "password", "secret", "key", "token", "auth",
            "api_key", "private_key", "access_token"
        ],
        "max_input_size": 500000,           # 500KB max
        "enable_sensitive_redaction": True,
        "redaction_placeholder": "[REDACTED]"
    }
)
```

### **Resource Limits (Security)**

```python
config = IntegrationConfig(
    security_limits={
        "max_processing_time": 300,         # Prevent runaway processes
        "max_memory_usage": 100 * 1024 * 1024,  # 100MB hard limit
        "max_field_count": 50,              # Prevent field explosion
        "max_attractor_count": 1000,        # Prevent attractor explosion
        "enable_resource_monitoring": True
    }
)
```

---

## 🎛️ **Command Line Configuration**

### **CLI Options**

```bash
# Basic usage with config override
python main_enhanced.py /path/to/project \
    --context-engineering \
    --optimization-mode efficiency \
    --memory-limit 50 \
    --timeout 120

# Disable specific features
python main_enhanced.py /path/to/project \
    --no-field-dynamics \
    --no-cognitive-tools \
    --atomic-prompting-only

# Configuration file override
python main_enhanced.py /path/to/project \
    --config config/production.json

# Environment override
CONTEXT_ENGINEERING_MODE=depth python main_enhanced.py /path/to/project
```

### **Programmatic CLI Configuration**

```python
import argparse
from main_enhanced import EnhancedCursorRulesProjectAnalyzer
from core.context_engineering.integration_manager import IntegrationConfig

def create_custom_analyzer(args):
    config = IntegrationConfig(
        optimization_mode=args.mode,
        field_capacity=args.field_capacity,
        max_processing_time=args.timeout,
        error_tolerance_level=args.error_tolerance
    )
    
    return EnhancedCursorRulesProjectAnalyzer(
        enable_context_engineering=args.enable_context_engineering,
        integration_config=config
    )

# Parse arguments and create analyzer
parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['efficiency', 'depth', 'balanced'], default='balanced')
parser.add_argument('--field-capacity', type=int, default=8000)
parser.add_argument('--timeout', type=int, default=300)
parser.add_argument('--error-tolerance', choices=['strict', 'moderate', 'permissive'], default='moderate')

args = parser.parse_args()
analyzer = create_custom_analyzer(args)
```

---

## 🔄 **Configuration Validation and Testing**

### **Validate Configuration**

```python
from core.context_engineering.integration_manager import IntegrationConfig, validate_context_engineering_dependencies

def validate_configuration():
    try:
        # Test configuration
        config = IntegrationConfig(
            optimization_mode="balanced",
            field_capacity=8000,
            token_efficiency_threshold=0.7
        )
        print("✅ Configuration valid")
        
        # Test dependencies
        deps_ok, issues = validate_context_engineering_dependencies()
        if deps_ok:
            print("✅ Dependencies satisfied")
        else:
            print(f"⚠️ Dependency issues: {issues}")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")

validate_configuration()
```

### **Test Configuration Performance**

```python
import time
from main_enhanced import EnhancedCursorRulesProjectAnalyzer

async def test_configuration_performance(config):
    start_time = time.time()
    
    analyzer = EnhancedCursorRulesProjectAnalyzer(
        enable_context_engineering=True,
        integration_config=config
    )
    
    # Test with small project
    results = await analyzer.run_analysis(".")
    
    end_time = time.time()
    
    return {
        "processing_time": end_time - start_time,
        "enhancement_level": results.get("_global_enhancement_metadata", {}).get("enhancement_level"),
        "memory_usage": analyzer.get_system_status().get("integration_manager_status", {}),
        "success": not results.get("error")
    }

# Test different configurations
configs = {
    "efficiency": IntegrationConfig(optimization_mode="efficiency"),
    "balanced": IntegrationConfig(optimization_mode="balanced"),
    "depth": IntegrationConfig(optimization_mode="depth")
}

for name, config in configs.items():
    result = await test_configuration_performance(config)
    print(f"{name}: {result}")
```

---

## 📚 **Configuration Best Practices**

### **1. Start with Defaults**
The system is pre-configured for optimal performance. Only change settings when you have specific requirements.

### **2. Environment-Specific Configs**
Use different configurations for different environments:
- **Development**: Higher timeouts, debug logging, strict error handling
- **Testing**: Moderate settings, comprehensive metrics
- **Production**: Efficiency mode, error tolerance, monitoring

### **3. Gradual Optimization**
1. Start with default configuration
2. Monitor performance and resource usage
3. Adjust one parameter at a time
4. Test changes thoroughly
5. Document what works for your use case

### **4. Monitor and Alert**
- Enable health checks and metrics
- Set up alerts for degraded performance
- Monitor resource usage trends
- Track enhancement success rates

### **5. Security First**
- Always enable input sanitization
- Set reasonable resource limits
- Monitor for unusual activity
- Regularly update dependency validation

---

**🎉 You now have complete control over the Enhanced CursorRules Architect configuration!**

The system provides extensive customization while maintaining safety and reliability. Start with the defaults and adjust based on your specific needs and constraints.

*Next: Learn about [Performance Tuning](./performance-tuning.md) to optimize your configuration for maximum efficiency.*