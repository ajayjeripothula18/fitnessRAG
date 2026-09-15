# Integration Plan: Startup MVP Build Agent Skills with RRPAI Workflow

## Meeting Context
This document captures the team discussion on how to integrate the Startup MVP Build agent skills from `.agents/skills/` into the existing RRPAI workflow in `.agent/workflows/` while maintaining alignment with project personas in `.project/personas/`.

**Meeting Participants**: All team members as defined in team-meeting.md
**Purpose**: Plan integration of specialized agent skills into RRPAI workflow phases
**Approach**: Follow team-meeting.md discussion format with decision logging per Karan (BA)

---

## Discussion Transcript

### Opening
**Karan (BA)**: "Let me recap where we stand. We have our established RRPAI workflow with 7 phases, our team personas with specific roles, and a set of specialized agent skills in `.agents/skills/`. The goal is to integrate these skills into our workflow phases without changing the core RRPAI structure - just attaching appropriate skills to each phase and aligning with our personas."

**Priya (CPO)**: "Sets the agenda: We need to determine which agent skills belong in each RRPAI phase, how they map to our personas, and what documentation changes we need to make to the workflow files to indicate these integrations."

### Discussion

**Priya (CPO)**: "Starting with business perspective - in REVIEW phase, we need to understand requirements. The project-manager-senior skill is perfect for specification analysis and requirements extraction. Evidence-collector can gather existing project documentation. For persona alignment, I (CPO) should own the business requirements aspect of REVIEW."

**Arjun (CTO)**: "From technical architecture standpoint, in REVIEW we also need ux-architect to review user experience requirements and agents-orchestrator to coordinate the review process. I (CTO) should oversee the technical feasibility aspects. Brand-guardian and analytics-reporter could provide secondary support for brand alignment and initial metrics assessment."

**Ravi (TechLead)**: "In RESEARCH phase, we need market and technical validation. Growth-hacker for market research, content-creator for competitive analysis, ai-engineer for AI/ML technology research, and social-media-strategist for community insights. Evidence-collector can do deep dive evidence gathering. I should focus on the technical validation aspects while collaborating with the AI Engineer skill."

**Meera (Backend)**: "For PLAN phase, project-manager-senior creates the structured task list from requirements - this is core to my backend planning responsibilities. Ux-architect creates the CSS design system, layout framework, and UX foundation which I need for API contracts. Sprint-prioritizer handles feature prioritization which I collaborate on with backend capacity planning. Brand-guardian ensures architectural decisions align with our brand. I should own the technical planning aspects."

**Zara (Frontend)**: "In PLAN, I (Frontend Lead) work closely with ux-architect on the design system and layout framework. I also contribute to sprint prioritization from frontend capacity perspective. Brand-guardian is critical for ensuring our UI/UX maintains brand consistency. Rapid-prototyper could be useful for creating quick UI validation prototypes."

**Vikram (QA/DevOps)**: "In APPROVE phase, project-manager-senior presents the plan and manages the approval process - I need to ensure the plan includes testable acceptance criteria. Ux-architect validates the UX/architecture designs. Priya (CPO) gives the final business approval. Agents-orchestrator coordinates the approval workflow and evidence-collector provides evidence for decision-making. I focus on ensuring the plan includes adequate testing and quality gates."

**Karan (BA)**: "For IMPLEMENT phase, this is where skills get task-specific. Frontend-developer handles UI/UX implementation (my frontend stories), backend-architect handles server-side architecture (backend stories), devops-automator handles infrastructure/tasks, ai-engineer handles AI/ML models, rapid-prototyper does proof-of-concepts. Agents-orchestrator orchestrates the handoffs between these agents. As Scrum Master, I track progress in our sprint tracker and ensure Definition of Done is followed."

**Meera (Backend)**: "In VALIDATE phase, evidence-collector collects test evidence and documentation - this aligns with my backend testing responsibilities. Reality-checker does final validation. Performance-benchmarker does performance testing (important for our API latency goals). Api-tester validates our APIs. Workflow-optimizer analyzes our processes. I should coordinate the backend validation aspects."

**Arjun (CTO)**: "In ITERATE phase, agents-orchestrator coordinates the iteration process. Project-manager-senior updates plans/tasks based on findings. Evidence-collector collects evidence of issues/failures. Workflow-optimizer analyzes processes for improvements. Ux-architect revises UX/architecture if design flaws were found. Rapid-prototyper quickly prototypes solutions for validation. As CTO, I ensure technical soundness of any architectural changes made during iteration."

### Decision Logging (Karan - BA)

**✅ Decision Made**: 
- Map specific agent skills to each RRPAI phase based on their core competencies
- Align each skill with relevant project personas for clear ownership
- Add skill mapping documentation to each workflow file without changing core processes
- Maintain the mandatory checkpoint protocol and session logging requirements

**❓ Open Question**: 
- Should we create a centralized skills registry document, or keep mappings distributed in each workflow file?
- How detailed should the skill invocation instructions be in each workflow phase?

**🚫 Rejected**: 
- Changing the core RRPAI phase structure or sequence
- Removing any existing workflow documentation or templates
- Making the skill mappings mandatory (they should be guidance, not requirements)

**📌 Action Items**:
1. Create skill mapping documentation for each workflow phase (REVIEW through ITERATE)
2. Update each workflow file to include a "Skill Mapping for This Phase" section
3. Ensure persona alignments are clearly documented
4. Preserve all existing workflow content and structure
5. Validate that mapping doesn't interfere with existing tool commands or turbo annotations

**⚠️ Risk Flagged**: 
- Overcomplicating the workflow with too many skill references
- Creating confusion about when to invoke skills vs. follow standard process
- Inconsistent application across different team members

## Skill-to-Phase Mapping Summary

### **REVIEW Phase**
- **Primary Skills**: project-manager-senior, evidence-collector, ux-architect, agents-orchestrator
- **Secondary Skills**: brand-guardian, analytics-reporter
- **Persona Alignment**: 
  * Priya (CPO): Business requirement validation
  * Arjun (CTO): Technical feasibility oversight
  * Meera (Backend): Backend requirements review
  * Zara (Frontend): UX requirements input
  * Vikram (QA/DevOps): Testing context assessment
  * Karan (BA): Process facilitation

### **RESEARCH Phase**
- **Primary Skills**: growth-hacker, content-creator, ai-engineer, social-media-strategist
- **Secondary Skills**: evidence-collector
- **Persona Alignment**:
  * Priya (CPO): Market fit and user persona validation
  * Arjun (CTO): Technical approach validation
  * Ravi (TechLead): AI/ML research leadership
  * Zara (Frontend): User workflow and design research
  * Vikram (QA/DevOps): Research validation for testability
  * Karan (BA): Research process documentation

### **PLAN Phase**
- **Primary Skills**: project-manager-senior, ux-architect, sprint-prioritizer, brand-guardian
- **Secondary Skills**: rapid-prototyper, evidence-collector
- **Persona Alignment**:
  * Priya (CPO): Business priority validation and backlog refinement
  * Arjun (CTO): Technical architecture oversight
  * Ravi (TechLead): Implementation planning contribution
  * Meera (Backend): Backend planning and API design
  * Zara (Frontend): UX/UI planning and design system
  * Vikram (QA/DevOps): Validation and test planning
  * Karan (BA): Sprint planning and task breakdown facilitation

### **APPROVE Phase**
- **Primary Skills**: project-manager-senior, ux-architect
- **Secondary Skills**: priya-cpo persona (business approval), agents-orchestrator, evidence-collector
- **Persona Alignment**:
  * Priya (CPO): Final business/product approval
  * Arjun (CTO): Technical architecture approval
  * Ravi (TechLead): Implementation feasibility sign-off
  * Meera (Backend): API contract approval
  * Zara (Frontend): UX/design approval
  * Vikram (QA/DevOps): Test plan approval
  * Karan (BA): Approval process facilitation

### **IMPLEMENT Phase**
- **Primary Skills** (task-dependent):
  * frontend-developer - UI/UX implementation
  * backend-architect - Server-side architecture/API
  * devops-automator - Infrastructure/deployment/CI/CD
  * ai-engineer - AI/ML model development
  * rapid-prototyper - Proof-of-concept/spike solutions
- **Coordination Skill**: agents-orchestrator
- **Persona Alignment**:
  * Priya (CPO): Business value validation of implementations
  * Arjun (CTO): Technical implementation oversight
  * Ravi (TechLead): Full-stack implementation coordination
  * Meera (Backend): Backend implementation execution
  * Zara (Frontend): Frontend implementation execution
  * Vikram (QA/DevOps): Quality assurance and test execution
  * Karan (BA): Process facilitation and impediment removal

### **VALIDATE Phase**
- **Primary Skills**: evidence-collector, reality-checker, performance-benchmarker, api-tester, workflow-optimizer
- **Secondary Skills**: ux-architect, brand-guardian
- **Persona Alignment**:
  * Priya (CPO): Business value validation
  * Arjun (CTO): Technical validation and architecture review
  * Ravi (TechLead): Implementation quality assessment
  * Meera (Backend): Backend testing and validation
  * Zara (Frontend): UX/UI validation and usability testing
  * Vikram (QA/DevOps): Test execution and quality gate enforcement
  * Karan (BA): Validation process facilitation and documentation

### **ITERATE Phase**
- **Primary Skills**: agents-orchestrator, project-manager-senior, evidence-collector, workflow-optimizer
- **Secondary Skills**: ux-architect, rapid-prototyper
- **Persona Alignment**:
  * Priya (CPO): Business impact assessment of changes
  * Arjun (CTO): Technical soundness of architectural changes
  * Ravi (TechLead): Implementation coordination for fixes
  * Meera (Backend): Backend fix implementation and testing
  * Zara (Frontend): Frontend fix implementation and validation
  * Vikram (QA/DevOps): Regression testing and quality assurance
  * Karan (BA): Iteration process facilitation and documentation

## Implementation Approach

To integrate these mappings without changing core workflows:

1. **Add Skill Mapping Sections**: Append a "Skill Mapping for This Phase" section to each workflow file in `.agent/workflows/` following the team discussion format
2. **Preserve Existing Content**: Make no changes to existing workflow steps, decision criteria, or tool commands
3. **Maintain Backward Compatibility**: All existing workflows continue to function exactly as before
4. **Provide Guidance Only**: Skill mappings serve as recommendations, not requirements
5. **Align with Personas**: Clearly show which team member persona has primary responsibility for each skill integration

## Next Steps

Upon team approval of this plan:
1. Implement the skill mapping documentation in each workflow file
2. Verify that all existing workflows continue to function as expected
3. Begin using the integrated skills in upcoming sprint planning and execution
4. Monitor effectiveness and adjust mappings as needed in future retrospectives

This integration enhances our RRPAI workflow with specialized expertise while preserving its core structure and mandatory checkpoints.