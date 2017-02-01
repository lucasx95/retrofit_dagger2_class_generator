package exp.bussiness;

public interface ExampleUseCases {

	Example createExample(final ExampleDto exampleDto) throws GeneralBusinessErrorException;

	List<Example> getAllExamplesFiltered(final Long testId, final String begin, final String end, final String status) throws GeneralBusinessErrorException;

	Void testExample(final ExampleDto exampleDto) throws GeneralBusinessErrorException;

}