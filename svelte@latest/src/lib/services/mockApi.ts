/**
 * Mock API Service
 *
 * This service provides mock implementations of API endpoints for development and testing.
 * It simulates API responses without making actual network requests.
 */

// Generate a mock ID for new items
const generateMockId = (): number => Math.floor(Math.random() * 1000) + 1;

// Get current timestamp in ISO format
const getCurrentTimestamp = (): string => new Date().toISOString();

/**
 * Mock API handler for future plans
 */
export const mockFuturePlanApi = {
  /**
   * Get all future plans
   */
  getAll: () => {
    const timestamp = getCurrentTimestamp();
    return [
      {
        id: 1,
        user_id: 1,
        title: "Learn a new programming language",
        description: "I want to learn Python to expand my programming skills and build data science projects.",
        goal_type: "Skill Development",
        target_date: "2023-12-31",
        status: "active" as "active" | "achieved" | "deferred" | "abandoned",
        created_at: timestamp,
        updated_at: timestamp
      },
      {
        id: 2,
        user_id: 1,
        title: "Complete personal project",
        description: "Finish building my portfolio website with all the latest projects and skills.",
        goal_type: "Project",
        target_date: "2023-10-15",
        status: "active" as "active" | "achieved" | "deferred" | "abandoned",
        created_at: timestamp,
        updated_at: timestamp
      },
      {
        id: 3,
        user_id: 1,
        title: "Attend tech conference",
        description: "Participate in the annual tech conference to network and learn about new technologies.",
        goal_type: "Career Development",
        target_date: "2023-11-05",
        status: "active" as "active" | "achieved" | "deferred" | "abandoned",
        created_at: timestamp,
        updated_at: timestamp
      }
    ];
  },

  /**
   * Get a single future plan by ID
   */
  getById: (id: number) => {
    const timestamp = getCurrentTimestamp();
    return {
      id,
      user_id: 1,
      title: "Mock future plan",
      description: "This is a detailed description of the mock future plan.",
      goal_type: "Career",
      target_date: "2023-12-31",
      status: "active" as "active" | "achieved" | "deferred" | "abandoned",
      created_at: timestamp,
      updated_at: timestamp
    };
  },

  /**
   * Create a new future plan
   */
  create: (data: any) => {
    const timestamp = getCurrentTimestamp();
    const status = (data.status || "active") as "active" | "achieved" | "deferred" | "abandoned";
    return {
      id: generateMockId(),
      user_id: 1,
      title: data.title,
      description: data.description,
      goal_type: data.goal_type || null,
      target_date: data.target_date || null,
      status,
      created_at: timestamp,
      updated_at: timestamp
    };
  },

  /**
   * Update an existing future plan
   */
  update: (id: number, data: any) => {
    const timestamp = getCurrentTimestamp();
    const status = (data.status || "active") as "active" | "achieved" | "deferred" | "abandoned";
    return {
      id,
      user_id: 1,
      title: data.title || "Updated plan title",
      description: data.description || "Updated plan description",
      goal_type: data.goal_type || null,
      target_date: data.target_date || null,
      status,
      created_at: timestamp,
      updated_at: timestamp
    };
  },

  /**
   * Delete a future plan
   */
  delete: () => {
    return {};
  }
};

/**
 * Mock API handler for achievements
 */
export const mockAchievementApi = {
  /**
   * Get all achievements
   */
  getAll: () => {
    const timestamp = getCurrentTimestamp();
    return [
      {
        id: 1,
        user_id: 1,
        title: "Completed project X",
        description: "Successfully delivered project X ahead of schedule",
        quantifiable_results: "Saved $10,000 in costs",
        core_skills_json: ["Project Management", "Leadership"],
        date_achieved: "2023-01-15",
        created_at: timestamp,
        updated_at: timestamp
      },
      {
        id: 2,
        user_id: 1,
        title: "Learned new technology",
        description: "Mastered a new programming framework",
        quantifiable_results: "Reduced development time by 30%",
        core_skills_json: ["Technical Skills", "Learning"],
        date_achieved: "2023-02-20",
        created_at: timestamp,
        updated_at: timestamp
      }
    ];
  },

  /**
   * Get a single achievement by ID
   */
  getById: (id: number) => {
    const timestamp = getCurrentTimestamp();
    return {
      id,
      user_id: 1,
      title: "Mock achievement",
      description: "This is a mock achievement",
      quantifiable_results: "Improved efficiency by 20%",
      core_skills_json: ["Communication", "Leadership"],
      date_achieved: "2023-01-15",
      created_at: timestamp,
      updated_at: timestamp
    };
  },

  /**
   * Create a new achievement
   */
  create: (data: any) => {
    const timestamp = getCurrentTimestamp();
    return {
      id: generateMockId(),
      user_id: 1,
      title: data.title,
      description: data.description || null,
      quantifiable_results: data.quantifiable_results || null,
      core_skills_json: data.core_skills_json || [],
      date_achieved: data.date_achieved || null,
      created_at: timestamp,
      updated_at: timestamp
    };
  },

  /**
   * Update an existing achievement
   */
  update: (id: number, data: any) => {
    const timestamp = getCurrentTimestamp();
    return {
      id,
      user_id: 1,
      title: data.title,
      description: data.description || null,
      quantifiable_results: data.quantifiable_results || null,
      core_skills_json: data.core_skills_json || [],
      date_achieved: data.date_achieved || null,
      created_at: timestamp,
      updated_at: timestamp
    };
  },

  /**
   * Delete an achievement
   */
  delete: () => {
    return {};
  }
};
