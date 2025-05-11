import gradio as gr
import pandas as pd
import random
from datetime import datetime, timedelta

# Generate dummy data
def generate_dummy_data(num_records=1000):
    courts = ["Supreme Court", "Bombay High Court", "Delhi High Court", "Madras High Court", "Calcutta High Court", 
              "Karnataka High Court", "Allahabad High Court", "Gujarat High Court", "Punjab & Haryana High Court"]
    
    judges = ["Justice A.K. Sikri", "Justice D.Y. Chandrachud", "Justice Sanjiv Khanna", "Justice Rohinton Nariman",
              "Justice Indu Malhotra", "Justice N.V. Ramana", "Justice Ranjan Gogoi", "Justice U.U. Lalit", 
              "Justice S. Ravindra Bhat", "Justice B.R. Gavai"]
    
    acts = ["Indian Penal Code", "Constitution of India", "Code of Criminal Procedure", "Income Tax Act",
            "Goods and Services Tax Act", "Prevention of Corruption Act", "Companies Act", 
            "Negotiable Instruments Act", "Arbitration and Conciliation Act", "Hindu Marriage Act"]
    
    sections = ["Section 302", "Section 420", "Section 377", "Section 498A", "Section 376", "Section 307",
                "Article 14", "Article 21", "Article 32", "Section 138"]
    
    case_types = ["Criminal Appeal", "Civil Appeal", "Special Leave Petition", "Writ Petition", 
                  "Review Petition", "Curative Petition", "Transfer Petition", "Original Suit"]
    
    disposal_types = ["Disposed", "Pending", "Dismissed", "Allowed", "Partly Allowed", "Withdrawn", "Admission Stage"]
    
    stages = ["ADMISSION STAGE", "HEARING STAGE", "FINAL STAGE", "DISPOSED"]
    
    benches = ["Principal Bench", "Aurangabad Bench", "Nagpur Bench", "Delhi Bench", "Lucknow Bench"]
    
    petitioners = ["State of Maharashtra", "Union of India", "Income Tax Department", "Bharti Airtel Ltd.",
                  "Tata Motors", "Reliance Industries", "Mukesh Ambani", "Ratan Tata", "Common Cause", 
                  "People's Union for Civil Liberties"]
    
    respondents = ["Union of India", "State of Maharashtra", "Municipal Corporation of Delhi", "Vijay Mallya",
                  "Central Bureau of Investigation", "Enforcement Directorate", "Reserve Bank of India",
                  "Election Commission of India", "Securities and Exchange Board of India"]
    
    # Generate random dates for the past 5 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    
    data = []
    for i in range(num_records):
        court = random.choice(courts)
        judge = random.choice(judges)
        act = random.choice(acts)
        section = random.choice(sections)
        case_type = random.choice(case_types)
        case_no = random.randint(1, 9999)
        year = random.randint(2010, 2025)
        random_days = random.randint(0, (end_date - start_date).days)
        decision_date = start_date + timedelta(days=random_days)
        
        # Format date as string
        decision_date_str = decision_date.strftime("%d-%m-%Y")
        
        petitioner = random.choice(petitioners)
        respondent = random.choice(respondents)
        disposal_nature = random.choice(disposal_types)
        stage = random.choice(stages)
        bench = random.choice(benches)
        
        # Generate dummy case title
        case_title = f"{petitioner} vs {respondent}"
        
        # Generate some dummy text for judgement
        judgement_text = f"In the matter of {case_title}, the {court} has considered the arguments presented by both parties. The case pertains to {act} {section}. After due consideration, the court has decided to {disposal_nature.lower()} the petition."
        
        # Generate a dummy PDF link for the judgement
        # In a real application, these would be actual links to stored PDFs
        # pdf_link = f"https://judgements.ecourts.gov.in/pdfs/{court.lower().replace(' ', '_')}/{year}/{case_no}.pdf"
        pdf_link = "/home/shiva_123/case-prizm-frontend/43b7fbcdfaf949adb92e8553b0e8c50d849b113f8272b939420035696feeb31d1746440594.pdf"
        
        data.append({
            "Court": court,
            "Judge": judge,
            "Act": act,
            "Section": section,
            "Decision Date": decision_date_str,
            "Case Type": case_type,
            "Case No": case_no,
            "Year": year,
            "Petitioner": petitioner,
            "Respondent": respondent,
            "Disposal Nature": disposal_nature,
            "Case Title": case_title,
            "Judgement Text": judgement_text,
            "Stage": stage,
            "Bench": bench,
            "PDF Link": pdf_link
        })
    
    return pd.DataFrame(data)

# Create dummy data
df = generate_dummy_data(1500)

# Function to filter data based on inputs
def filter_data(court, bench, judge, act_section, decision_date_range, search_text, search_type, time_filter, 
                case_type, case_no, year, party, disposal_nature, search_method):
    filtered_df = df.copy()
    
    # Apply court filter
    if court and court != "ALL" and court != "Select Court":
        filtered_df = filtered_df[filtered_df["Court"] == court]
    
    # Apply bench filter
    if bench and bench != "Select Bench":
        filtered_df = filtered_df[filtered_df["Bench"] == bench]
    
    # Apply judge filter
    if judge:
        filtered_df = filtered_df[filtered_df["Judge"].str.contains(judge, case=False)]
    
    # Apply act/section filter
    if act_section:
        act_section_filter = (filtered_df["Act"].str.contains(act_section, case=False)) | \
                            (filtered_df["Section"].str.contains(act_section, case=False))
        filtered_df = filtered_df[act_section_filter]
    
    # Apply case type filter
    if case_type and case_type != "Select Case Subject":
        filtered_df = filtered_df[filtered_df["Case Type"] == case_type]
    
    # Apply case number filter
    if case_no:
        filtered_df = filtered_df[filtered_df["Case No"].astype(str).str.contains(case_no)]
    
    # Apply year filter
    if year:
        filtered_df = filtered_df[filtered_df["Year"].astype(str) == year]
    
    # Apply party (petitioner/respondent) filter
    if party:
        party_filter = (filtered_df["Petitioner"].str.contains(party, case=False)) | \
                       (filtered_df["Respondent"].str.contains(party, case=False))
        filtered_df = filtered_df[party_filter]
    
    # Apply disposal nature filter
    if disposal_nature and disposal_nature != "Select Disposal Nature":
        filtered_df = filtered_df[filtered_df["Disposal Nature"] == disposal_nature]
    
    # Apply date filter
    if time_filter and time_filter != "ALL":
        today = datetime.now()
        if time_filter == "Past Week":
            start_date = today - timedelta(days=7)
        elif time_filter == "Past Month":
            start_date = today - timedelta(days=30)
        elif time_filter == "Past Year":
            start_date = today - timedelta(days=365)
        elif time_filter == "Custom range" and decision_date_range and len(decision_date_range) == 2:
            try:
                start_date = datetime.strptime(decision_date_range[0], "%Y-%m-%d")
                end_date = datetime.strptime(decision_date_range[1], "%Y-%m-%d")
                
                # Convert the string dates in the dataframe to datetime objects
                filtered_df["Decision Date"] = pd.to_datetime(filtered_df["Decision Date"], format="%d-%m-%Y")
                filtered_df = filtered_df[(filtered_df["Decision Date"] >= start_date) & 
                                         (filtered_df["Decision Date"] <= end_date)]
                # Convert back to string format to avoid issues with displaying
                filtered_df["Decision Date"] = filtered_df["Decision Date"].dt.strftime("%d-%m-%Y")
            except (ValueError, TypeError):
                # If date parsing fails, just return the current filtered dataframe
                pass
            return filtered_df
        
        try:
            # Convert the string dates in the dataframe to datetime objects
            filtered_df["Decision Date"] = pd.to_datetime(filtered_df["Decision Date"], format="%d-%m-%Y")
            filtered_df = filtered_df[filtered_df["Decision Date"] >= start_date]
            # Convert back to string format to avoid issues with displaying
            filtered_df["Decision Date"] = filtered_df["Decision Date"].dt.strftime("%d-%m-%Y")
        except (ValueError, TypeError):
            # If date parsing fails, just return the current filtered dataframe
            pass
    
    # Apply text search
    if search_text:
        if search_method == "Exact Match":
            # Exact match search
            if search_type == "Phrase(s)":
                # Search for exact phrase
                text_filter = (filtered_df["Case Title"].str.contains(search_text, case=False)) | \
                             (filtered_df["Judgement Text"].str.contains(search_text, case=False))
            else:  # Any Words or All Words
                # Split the search text into words
                search_words = search_text.split()
                
                if search_type == "Any Words":
                    # Match any of the words
                    text_filter = filtered_df["Judgement Text"].apply(
                        lambda text: any(word.lower() in text.lower() for word in search_words)
                    )
                else:  # All Words
                    # Match all of the words
                    text_filter = filtered_df["Judgement Text"].apply(
                        lambda text: all(word.lower() in text.lower() for word in search_words)
                    )
        else:  # Semantic Search - simple simulation for demo
            # This is a simplified simulation of semantic search
            # In a real application, you would use embeddings or NLP algorithms
            relevant_terms = {
                "murder": ["killing", "homicide", "death", "deceased", "weapon"],
                "theft": ["stolen", "robbery", "burglary", "property", "took"],
                "fraud": ["deception", "misrepresentation", "cheating", "false", "misleading"],
                "corruption": ["bribe", "illegal gratification", "misconduct", "undue advantage"],
                "constitution": ["fundamental rights", "directive principles", "amendment", "article"],
                "divorce": ["marriage", "separation", "alimony", "matrimonial", "spouse"]
            }
            
            # Expand search text with related terms
            expanded_terms = set([search_text.lower()])
            for term in search_text.lower().split():
                if term in relevant_terms:
                    expanded_terms.update(relevant_terms[term])
            
            # Search for any of the expanded terms
            text_filter = filtered_df["Judgement Text"].apply(
                lambda text: any(term.lower() in text.lower() for term in expanded_terms)
            )
        
        filtered_df = filtered_df[text_filter]
    
    return filtered_df

# Create the Gradio interface
def create_interface():
    with gr.Blocks() as app:
        # Header
        with gr.Row():
            with gr.Column(scale=4):
                gr.Markdown("# 🏛️ DigiLawyer.ai\n## Case Prism")
        
        # Main search bar
        with gr.Row():
            
            with gr.Column(scale=3):
                search_text = gr.Textbox(label="Search within case", placeholder="Enter search text")
            # with gr.Column(scale=1):
            #     search_type = gr.Radio(
            #         choices=["Phrase(s)", "Any Words", "All Words"],
            #         value="Phrase(s)",
            #         label=""
            #     )
            with gr.Column(scale=1):
                search_method = gr.Radio(
                    choices=["Exact Match", "Semantic Search"],
                    value="Exact Match",
                    label="Search Method"
                )
        
        # Search method selection
        # with gr.Row():
        with gr.Row():
            with gr.Column():
                legal_terms = gr.Textbox(label="Legal Terms", placeholder="Enter Legal terms")
            with gr.Column():
                lawyers=  gr.Textbox(label="Lawyers", placeholder="Enter name of Lawyers")
            with gr.Column():
                citations = gr.Textbox(label="Citations", placeholder="Enter citations")
            with gr.Column():
                date_of_registeration_time_filter = gr.Radio(
                    choices=["ALL", "Past Week", "Past Month", "Past Year", "Custom range"],
                    value="ALL",
                    label="Date of Registeration"
                )
                # Use two separate date inputs
                with gr.Column(visible=False) as date_range_container:
                    start_date_of_registeration = gr.Textbox(label="Start Date (YYYY-MM-DD)", placeholder="YYYY-MM-DD")
                    end_date_of_registeration = gr.Textbox(label="End Date (YYYY-MM-DD)", placeholder="YYYY-MM-DD")

        # Filter options
        with gr.Row():
            with gr.Column():
                court_dropdown = gr.Dropdown(
                    choices=["ALL"] + sorted(df["Court"].unique().tolist()),
                    value="ALL",
                    label="Court"
                )
            with gr.Column():
                judge_textbox = gr.Textbox(label="Judge", placeholder="Enter Judge Name")
            with gr.Column():
                act_section = gr.Textbox(label="Act/Section", placeholder="Enter Act or Section")
            with gr.Column():
                time_filter = gr.Radio(
                    choices=["ALL", "Past Week", "Past Month", "Past Year", "Custom range"],
                    value="ALL",
                    label="Decision Date"
                )
                # Use two separate date inputs
                with gr.Column(visible=False) as date_range_container:
                    start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", placeholder="YYYY-MM-DD")
                    end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", placeholder="YYYY-MM-DD")
            with gr.Column():
                search_button = gr.Button("Search", variant="primary")
                reset_button = gr.Button("Reset")
        
        

                # Advanced court filter details
        with gr.Accordion("Case Details", open=False):
            with gr.Row():
                selected_court = gr.Dropdown(
                    choices=["Select Court", "Bombay High Court", "Delhi High Court", "Madras High Court"],
                    value="Bombay High Court",
                    label="Select Court"
                )
            # with gr.Row():
            #     bench_dropdown = gr.Dropdown(
            #         choices=["Select Bench", "Principal Bench", "Aurangabad Bench", "Nagpur Bench"],
            #         value="Select Bench",
            #         label="Select Bench"
            #     )
            with gr.Row():
                case_type_dropdown = gr.Dropdown(
                    choices=["Select Case Subject"] + sorted(df["Case Type"].unique().tolist()),
                    value="Select Case Subject",
                    label="Case Subject"
                )
            with gr.Accordion('Case id', open=True):
                with gr.Row():
                    with gr.Column():
                        case_no = gr.Textbox(label="Case Type", placeholder="Enter Case Type")
                    with gr.Column():
                        case_no = gr.Textbox(label="Case No", placeholder="Enter Case Number")
                    with gr.Column():
                        year = gr.Textbox(label="Case Year", placeholder="Enter Case Year")
            # with gr.Row():
            #     with gr.Column():
            #         case_no = gr.Textbox(label="Case No", placeholder="Enter Case Number")
            #     with gr.Column():
            #         year = gr.Textbox(label="Year", placeholder="Enter Year")
            with gr.Row():
                party = gr.Textbox(label="Party", placeholder="Enter Petitioner / Respondent")
            with gr.Row():
                disposal_dropdown = gr.Dropdown(
                    choices=["Select Disposal Nature"] + sorted(df["Disposal Nature"].unique().tolist()),
                    value="Select Disposal Nature",
                    label="Disposal Nature"
                )
        
        # Display area with results on left and PDF viewer on right
        with gr.Row():
            # Left column for results
            with gr.Column(scale=3):
                results_text = gr.Markdown("")
                results_table = gr.Dataframe(
                    headers=["Court", "Judge", "Case Title", "Case Type", "Case No", "Year", "Decision Date", "Disposal Nature", "Stage"],
                    interactive=True,  # Make the table interactive so users can click on rows
                    elem_id="results_table"
                )
            
            # Right column for PDF viewer
            with gr.Column(scale=2):
                pdf_viewer = gr.HTML(value="<div>Select a case to view the judgement</div>", label="Judgement PDF")
        

        # Store current search results
        state = gr.State([])
        
        # Handle custom date range visibility
        def update_date_range_visibility(choice):
            return gr.update(visible=(choice == "Custom range"))
        
        time_filter.change(update_date_range_visibility, inputs=time_filter, outputs=date_range_container)
        
        # Handle search button click
        def search_cases(court, judge, act_section, time_filter, start_date, end_date, search_text, search_type, 
                        search_method, selected_court, bench, case_type, case_no, year, party, disposal_nature):
            # Use selected_court if specified in the accordion, otherwise use the main court dropdown
            court_to_use = selected_court if selected_court != "Select Court" else court
            
            # Combine start and end date into a date range format if custom range is selected
            date_range = None
            if time_filter == "Custom range" and start_date and end_date:
                date_range = [start_date, end_date]
            
            filtered_data = filter_data(
                court_to_use, bench, judge, act_section, date_range, search_text, search_type, time_filter,
                case_type, case_no, year, party, disposal_nature, search_method
            )
            
            num_results = len(filtered_data)
            
            # Create the results text
            results_message = f"About {num_results} results ({random.uniform(0.5, 3):.1f} seconds)"
            
            # Select only the columns we want to display
            display_columns = ["Court", "Judge", "Case Title", "Case Type", "Case No", "Year", "Decision Date", "Disposal Nature", "Stage"]
            display_data = filtered_data[display_columns].head(100)  # Limit to first 100 results
            
            # Store the full results (including PDF links) for later use when a row is clicked
            full_results = filtered_data.to_dict('records')
            
            return results_message, display_data, full_results
        
        search_button.click(
            search_cases,
            inputs=[court_dropdown, judge_textbox, act_section, time_filter, start_date, end_date, 
                   search_text,  search_method,   
                   case_type_dropdown, case_no, year, party, disposal_dropdown],
            outputs=[results_text, results_table, state]
        )
        
        # Handle row click to show PDF
        def show_pdf(evt: gr.SelectData, results):
            if not results or evt.index[0] >= len(results):
                return "<div>No judgment available for this case</div>"
            
            selected_case = results[evt.index[0]]
            pdf_link = selected_case.get("PDF Link", "")
            
            if not pdf_link:
                return "<div>No judgment available for this case</div>"
            
            # In a real application, you might embed a PDF viewer here
            # For this demo, we'll create a simulated PDF viewer with HTML
            html = f"""
            <div style="border: 1px solid #ccc; padding: 20px; border-radius: 5px;">
                <h2>{selected_case['Case Title']}</h2>
                <p><strong>Court:</strong> {selected_case['Court']}</p>
                <p><strong>Judge:</strong> {selected_case['Judge']}</p>
                <p><strong>Case No:</strong> {selected_case['Case No']}/{selected_case['Year']}</p>
                <p><strong>Decision Date:</strong> {selected_case['Decision Date']}</p>
                <hr/>
                <div style="background-color: #f9f9f9; padding: 15px; font-family: serif;">
                    <p>{selected_case['Judgement Text']}</p>
                    <p>This judgment relates to {selected_case['Act']} {selected_case['Section']}.</p>
                    <p>After considering all aspects of the case, the court decided to {selected_case['Disposal Nature'].lower()} the petition.</p>
                </div>
                <hr/>
                <p>
                    <a href="{pdf_link}" target="_blank" style="background-color: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px;">
                        Download Full Judgment PDF
                    </a>
                </p>
            </div>
            """
            return html
        
        results_table.select(show_pdf, inputs=[state], outputs=[pdf_viewer])
        
        # Handle reset button click
        def reset_filters():
            return ("ALL", "", "", "ALL", "", "", "", "Phrase(s)", "Exact Match", 
                   "Bombay High Court", "Select Bench", "Select Case Subject", "", "", 
                   "", "Select Disposal Nature", "", None, [], "<div>Select a case to view the judgement</div>")
        
        reset_button.click(
            reset_filters,
            inputs=[],
            outputs=[court_dropdown, judge_textbox, act_section, time_filter, start_date, end_date, 
                    search_text,  search_method,   
                    case_type_dropdown, case_no, year, party, disposal_dropdown,
                    results_text, results_table, state, pdf_viewer]
        )
    
    return app

# Launch the app
if __name__ == "__main__":
    app = create_interface()
    app.launch(debug=True)