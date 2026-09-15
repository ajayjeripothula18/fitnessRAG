# Team Meeting: Docker Build Performance Issue

**Date**: 2026-09-07
**Participants**: Priya (CPO), Arjun (CTO), Ravi (Tech Lead), Meera (Senior Backend Engineer), Zara (Senior Frontend Engineer & UX Lead), Vikram (QA Lead & DevOps), Karan (Business Analyst & Scrum Master)

## Meeting Simulation

**Karan (BA)**: "Let's start with a quick recap. In our last discussion, we identified that the Docker build for the fitnessrag backend was taking over 5 hours, which was blocking our Sprint 1 closure. We traced this to the `--no-cache-dir` flag in the Dockerfile that was preventing pip from using its download cache. The fix was to remove this flag to restore normal caching behavior. Has anyone verified that this fix is in place?"

**Priya (CPO)**: "Thanks for the recap, Karan. Before we dive into the technical details, let me ask: why does this Docker build performance matter from a product perspective? Who is this actually for and why would they care?"

**Arjun (CTO)**: "From a product standpoint, slow builds directly impact our ability to iterate and deliver value. If developers are waiting 5+ hours for every build, that's countless hours wasted per sprint that could be spent on actual feature development. It also affects our CI/CD pipeline - if tests take forever to run because of slow builds, we lose rapid feedback cycles."

**Ravi (Tech Lead)**: "I can confirm the fix is in place. I checked the Dockerfile earlier today and confirmed that the `--no-cache-dir` flag has been removed from the pip install command. We're now using `RUN pip install --user -r requirements.txt` which should allow pip to cache downloads and reuse them across builds."

**Meera (Senior Backend Engineer)**: "That's good to hear. From a backend perspective, this fix is critical because our requirements.txt includes heavy dependencies like torch and langchain packages. Without caching, each build was re-downloading these large packages, which explains the 5+ hour build times. With caching restored, subsequent builds should be much faster as they only need to download changed dependencies."

**Zara (Senior Frontend Engineer & UX Lead)**: "While I'm primarily focused on the frontend, I want to make sure we're aligned on the overall impact. Slow backend builds affect our ability to test end-to-end flows. If the backend takes forever to build and deploy, it slows down our frontend integration testing as well."

**Vikram (QA Lead & DevOps)**: "This is exactly the kind of day-2 operational concern I worry about. Beyond just fixing the build time, we should also consider:
1. Monitoring build times in our CI pipeline to catch regressions early
2. Setting up alerts if build times exceed a threshold (say 30 minutes)
3. Documenting this fix in our runbook so future team members understand why we don't use --no-cache-dir
4. Considering if we want to implement buildkit cache exports for even faster CI builds"

**Karan (BA)**: "Let me capture what we've discussed so far:

✅ **Decision Made**: Confirmed that the `--no-cache-dir` flag has been removed from the Dockerfile, which should resolve the 5+ hour build time issue by restoring pip's download caching.

❓ **Open Question**: How long should we expect the current build to take now that the fix is in place? And what's our plan if it's still taking too long?

🚫 **Rejected**: Keeping the --no-cache-dir flag (was causing excessive build times)

📌 **Action Items**:
1. Wait for the current Docker build to complete and verify it finishes in a reasonable time (<30 minutes)
2. If successful, proceed with manual testing for Sprint 1 signoff
3. Add build time monitoring to our CI pipeline
4. Document the Dockerfile change rationale in our documentation

**Founder (User)**: "I'm concerned that even with the fix, the build might still take too long due to the size of our dependencies, particularly torch. What if we're still looking at 2+ hour builds? Are there any additional optimizations we should consider?"

**Priya (CPO)**: "That's a valid concern. Let's think about this from a risk perspective. What's the worst case if builds are still slow? And what are our options if the simple cache fix isn't enough?"

**Arjun (CTO)**: "If builds are still taking 2+ hours after fixing the cache issue, we have a few options:
1. Use Docker build caching more effectively with buildkit
2. Consider multi-stage builds that separate dependency installation from application code copying
3. Pre-build and cache dependency layers in our CI pipeline
4. As a last resort, evaluate if we can reduce dependency size (though torch is likely necessary for our ML features)"

**Ravi (Tech Lead)**: "I've already looked at our Dockerfile and it's using a reasonably optimized multi-stage build. The dependency installation happens in the builder stage, and we copy only the installed packages to the runtime stage. This is already a good practice."

**Meera (Senior Backend Engineer)**: "From a backend perspective, I'd suggest we:
1. First verify how long the current build takes with the cache fix
2. If it's still too long, investigate using `--no-deps` flag strategically or caching the pip download directory
3. Consider using `pip freeze` to lock dependencies and reduce resolution time
4. Look into whether we can use pre-built wheels for torch instead of building from source"

**Vikram (QA Lead & DevOps)**: "From a DevOps standpoint, I'd recommend:
1. Setting up build caching in GitHub Actions using the `actions/cache` pip feature
2. Monitoring build metrics over time to trend improvements
3. Considering remote caching solutions if we continue to have issues
4. Making sure we have proper logging so we can diagnose where time is spent in the build"

**Karan (BA)**: "Let me update our action items based on this discussion:

✅ **Decision Made**: We'll proceed with verifying the current build time first, then implement additional optimizations only if needed.

❓ **Open Question**: What constitutes an acceptable build time for our team? Should we aim for under 10 minutes, 20 minutes, or is 30 minutes acceptable?

🚫 **Rejected**: Over-engineering the solution before verifying if the basic fix works.

📌 **Action Items** (updated):
1. Wait for the current Docker build to complete and verify finish time
2. If build completes in <30 minutes, consider it a success and move to manual testing
3. If build takes >30 minutes, investigate additional optimizations:
   - Implement pip caching in GitHub Actions
   - Consider dependency pre-caching strategies
   - Evaluate if we can optimize torch installation
4. Document build time expectations in our team agreement
5. Add build monitoring to CI pipeline

Now, let's hear if anyone has final thoughts before we conclude this discussion.""