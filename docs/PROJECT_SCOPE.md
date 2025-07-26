# [Project Name] - Project Scope

---

## **IMPORTANT: PROJECT CONTINUITY**  
To maintain project context across conversations, always start a new chat with the following instructions:  

```
You are working on the [project name here]
Read CHANGELOG.md and PROJECT_SCOPE.md now, report your findings, and strictly follow all instructions found in these documents.  
You must complete the check-in process before proceeding with any task.  

Begin check-in process and document analysis.
```

---

## **IMPORTANT: SELF-MAINTENANCE INSTRUCTIONS**  

### **Before Taking Any Action or Making Suggestions**  
1. **Read Both Files**:  
   - Read `CHANGELOG.md` and `PROJECT_SCOPE.md`.  
   - Immediately report:  
     ```
     Initializing new conversation...  
     Read [filename]: [key points relevant to current task]  
     Starting conversation history tracking...
     ```

2. **Review Context**:  
   - Assess existing features, known issues, and architectural decisions.  

3. **Inform Responses**:  
   - Use the gathered context to guide your suggestions or actions.  

4. **Proceed Only After Context Review**:  
   - Ensure all actions align with the project's scope and continuity requirements.

---

### **After Making ANY Code Changes**  
1. **Update Documentation Immediately**:  
   - Add new features/changes to the `[Unreleased]` section of `CHANGELOG.md`.  
   - Update `PROJECT_SCOPE.md` if there are changes to architecture, features, or limitations.

2. **Report Documentation Updates**:  
   - Use the following format to report updates:  
     ```
     Updated CHANGELOG.md: [details of what changed]  
     Updated PROJECT_SCOPE.md: [details of what changed] (if applicable)
     ```

3. **Ensure Alignment**:  
   - Verify that all changes align with existing architecture and features.

4. **Document All Changes**:  
   - Include specific details about:
     - New features or improvements
     - Bug fixes
     - Error handling changes
     - UI/UX updates
     - Technical implementation details

5. **Adhere to the Read-First/Write-After Approach**:  
   - Maintain explicit update reporting for consistency and continuity.

---

## **Project Overview**
A multi-phase codebase analysis tool leveraging various AI models (OpenAI, Anthropic, Gemini, and DeepSeek) to perform comprehensive project analysis.

---

## **Core Objectives**
1. Provide in-depth codebase analysis through multiple specialized phases
2. Support multiple AI providers for flexible analysis capabilities
3. Generate comprehensive analysis reports and recommendations
4. Enable extension of the system through APIs and tool integration

---

## **Technical Architecture**

### **Integrations**
- Anthropic Claude API
- OpenAI API
- Google Gemini API
- DeepSeek API

### **Functions**
- Multi-phase project analysis
- AI agent orchestration

### **UI Features**
- Command line interface with rich output formatting

### **User Features**
- Configurable analysis phases
- Model selection for different analysis steps

---

## **Data Structures**
- Analysis phases and results
- Agent configurations
